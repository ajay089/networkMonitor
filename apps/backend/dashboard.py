from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime, timedelta

class DashboardDataViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def list(self, request):
        try:
            # Query for your main dashboard data (unchanged)
            main_query = """
                SELECT
                    totalCountToday,
                    totalCountYesterday,
                    totalOutgoingToday,
                    totalOutgoingYesterday,
                    totalIncomingToday,
                    totalIncomingYesterday,
                    loginAttemptsToday,
                    loginAttemptsYesterday,
                    -- Comparisons: Is Today's count greater than Yesterday's?
                    (totalCountToday > totalCountYesterday) AS isTotalCountGreater,
                    (totalOutgoingToday > totalOutgoingYesterday) AS isTotalOutgoingGreater,
                    (totalIncomingToday > totalIncomingYesterday) AS isTotalIncomingGreater,
                    (loginAttemptsToday > loginAttemptsYesterday) AS isLoginAttemptsGreater,
                    -- Percentage Changes
                    IF(totalCountYesterday = 0 AND totalCountToday > 0, 100, IF(totalCountYesterday = 0, NULL, ((totalCountToday - totalCountYesterday) / totalCountYesterday * 100))) AS pctChangeTotalCount,
                    IF(totalOutgoingYesterday = 0 AND totalOutgoingToday > 0, 100, IF(totalOutgoingYesterday = 0, NULL, ((totalOutgoingToday - totalOutgoingYesterday) / totalOutgoingYesterday * 100))) AS pctChangeTotalOutgoing,
                    IF(totalIncomingYesterday = 0 AND totalIncomingToday > 0, 100, IF(totalIncomingYesterday = 0, NULL, ((totalIncomingToday - totalIncomingYesterday) / totalIncomingYesterday * 100))) AS pctChangeTotalIncoming,
                    IF(loginAttemptsYesterday = 0 AND loginAttemptsToday > 0, 100, IF(loginAttemptsYesterday = 0, NULL, ((loginAttemptsToday - loginAttemptsYesterday) / loginAttemptsYesterday * 100))) AS pctChangeLoginAttempts
                FROM (
                    SELECT
                        SUM(CASE WHEN date = CURDATE() THEN 1 ELSE 0 END) AS totalCountToday,
                        SUM(CASE WHEN date = CURDATE() - INTERVAL 1 DAY THEN 1 ELSE 0 END) AS totalCountYesterday,
                        SUM(CASE WHEN date = CURDATE() AND action = 'deny' THEN 1 ELSE 0 END) AS totalOutgoingToday,
                        SUM(CASE WHEN date = CURDATE() - INTERVAL 1 DAY AND action = 'deny' THEN 1 ELSE 0 END) AS totalOutgoingYesterday,
                        SUM(CASE WHEN date = CURDATE() AND action = 'accept' THEN 1 ELSE 0 END) AS totalIncomingToday,
                        SUM(CASE WHEN date = CURDATE() - INTERVAL 1 DAY AND action = 'accept' THEN 1 ELSE 0 END) AS totalIncomingYesterday,
                        SUM(CASE WHEN date = CURDATE() AND subtype = 'login_attempt' THEN 1 ELSE 0 END) AS loginAttemptsToday,
                        SUM(CASE WHEN date = CURDATE() - INTERVAL 1 DAY AND subtype = 'login_attempt' THEN 1 ELSE 0 END) AS loginAttemptsYesterday
                    FROM logs
                ) AS daily_counts;
            """

            # Dynamic date range for bandwidth data
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=6)  # Example: Last 7 days

            bandwidth_query = """
                WITH RECURSIVE DateRange AS (
                    SELECT DATE(%s) AS date
                    UNION ALL
                    SELECT DATE_ADD(date, INTERVAL 1 DAY)
                    FROM DateRange
                    WHERE date < DATE(%s)
                )
                SELECT
                    d.date,
                    COALESCE(SUM(l.sentbyte) / 1048576, 0) AS total_sent_bytes
                FROM DateRange d
                LEFT JOIN logs l ON d.date = l.date
                GROUP BY d.date
                ORDER BY d.date;
            """

            with connection.cursor() as cursor:
                cursor.execute(main_query)
                main_row = cursor.fetchone()

                cursor.execute(bandwidth_query, [start_date, end_date])
                bandwidth_rows = cursor.fetchall()

            if main_row:
                columns = [
                    'totalCountToday', 'totalCountYesterday', 'totalOutgoingToday', 'totalOutgoingYesterday',
                    'totalIncomingToday', 'totalIncomingYesterday', 'loginAttemptsToday', 'loginAttemptsYesterday',
                    'isTotalCountGreater', 'isTotalOutgoingGreater', 'isTotalIncomingGreater', 'isLoginAttemptsGreater',
                    'pctChangeTotalCount', 'pctChangeTotalOutgoing', 'pctChangeTotalIncoming', 'pctChangeLoginAttempts'
                ]
                main_data = dict(zip(columns, main_row))

                # Process bandwidth data
                bandwidth_data = {}
                for row in bandwidth_rows:
                    date_str = row[0].strftime('%Y-%m-%d')  # Convert date to string
                    bandwidth_data[date_str] = row[1]

                # Ensure all dates within range are included and set to 0 if data is missing
                current_date = start_date
                while current_date <= end_date:
                    date_str = current_date.strftime('%Y-%m-%d')
                    if date_str not in bandwidth_data:
                        bandwidth_data[date_str] = 0
                    current_date += timedelta(days=1)

                # Add bandwidth data to main_data
                main_data['bandwidthData'] = bandwidth_data

                return Response(main_data)
            else:
                return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist as e:
            return Response({"detail": "Object does not exist."}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
