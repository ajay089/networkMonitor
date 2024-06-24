from datetime import datetime, timedelta
from django.db import connection
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
import concurrent.futures

class DashboardDataViewSet(viewsets.ViewSet):
    # Define main query for dashboard data
    def fetch_dashboard_data(self):
        try:
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
            with connection.cursor() as cursor:
                cursor.execute(main_query)
                main_row = cursor.fetchone()
            return main_row if main_row else None
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Define query for bandwidth data
    def fetch_bandwidth_data(self, start_date, end_date):
        try:
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
                cursor.execute(bandwidth_query, [start_date, end_date])
                bandwidth_rows = cursor.fetchall()
            return bandwidth_rows
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Define query for level-wise counts
    def fetch_level_data(self, start_date, end_date):
        try:
            days_ago = end_date - timedelta(days=7)
            level_query = """
                SELECT
                    date,
                    level,
                    COUNT(*) AS count
                FROM logs
                WHERE date >= %s
                GROUP BY date, level
                ORDER BY date DESC;
            """
            with connection.cursor() as cursor:
                cursor.execute(level_query, [days_ago])
                level_rows = cursor.fetchall()
            return level_rows
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Define query for traffic event summary type data
    def fetch_traffic_event_data(self, start_date, end_date):
        try:
            traffic_event_query = """
                SELECT type, subtype, COUNT(id) as event_count
                FROM logs
                WHERE date BETWEEN %s AND %s
                GROUP BY type, subtype
                ORDER BY event_count DESC;
            """
            with connection.cursor() as cursor:
                cursor.execute(traffic_event_query, [start_date, end_date])
                traffic_event_rows = cursor.fetchall()
            return traffic_event_rows
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Define query for server wise log data
    def fetch_server_wise_log_data(self, start_date, end_date):
        try:
            server_wise_log_query = """
                SELECT devname, COUNT(*) AS total
                FROM logs
                WHERE date BETWEEN %s AND %s
                GROUP BY devname
                ORDER BY total DESC
                LIMIT 10;
            """
            with connection.cursor() as cursor:
                cursor.execute(server_wise_log_query, [start_date, end_date])
                server_wise_log_rows = cursor.fetchall()

            # Convert rows to list of dicts
            server_wise_log_data = [
                {'devname': row[0], 'total': row[1]} for row in server_wise_log_rows
            ]
            return server_wise_log_data
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

         
    # Format data for response
    def format_data(self, main_row, bandwidth_rows, level_rows, traffic_event_rows, server_wise_log_data_rows, start_date, end_date):
        try:
            if not main_row:
                return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)

            # Process main query result
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

            # Process level data
            level_data = {}
            for row in level_rows:
                date_str = row[0].strftime('%Y-%m-%d') 
                level = row[1]
                count = row[2]

                if date_str not in level_data:
                    level_data[date_str] = {}

                level_data[date_str][level] = count

            # Ensure all dates within the last 7 days are included
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                if date_str not in level_data:
                    level_data[date_str] = {}

                current_date += timedelta(days=1)
            
            # Convert level_data to match the desired JSON structure
            level_data_formatted = []
            for date_str in sorted(level_data.keys()):
                formatted_level_data = {}
                for level, count in level_data[date_str].items():
                    formatted_level_data[level] = count
                level_data_formatted.append({
                    'date': datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %B'),
                    'level_data': formatted_level_data
                })

            # Add level_data to main_data in descending date order
            main_data['level_data'] = level_data_formatted

            # Process traffic_event data
            traffic_event_data = {}
            for row in traffic_event_rows:
                type_ = row[0].capitalize()
                subtype = row[1].capitalize()
                event_count = row[2]

                if type_ not in traffic_event_data:
                    traffic_event_data[type_] = {}

                traffic_event_data[type_][subtype] = event_count

            # Add traffic_event_data to main_data
            main_data['traffic_event_data'] = traffic_event_data

            main_data['server_wise_log_data_rows'] = server_wise_log_data_rows
            return main_data
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Implement list view
    def list(self, request):
        try:
            end_date    = datetime.now().date()
            start_date  = end_date - timedelta(days=6)  # Example: Last 7 days

            # Execute queries in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_dashboard_data           = executor.submit(self.fetch_dashboard_data)
                future_bandwidth_data           = executor.submit(self.fetch_bandwidth_data, start_date, end_date)
                future_level_data               = executor.submit(self.fetch_level_data, start_date, end_date)
                future_traffic_event_data       = executor.submit(self.fetch_traffic_event_data, start_date, end_date)
                fetch_server_wise_log_data      = executor.submit(self.fetch_server_wise_log_data, start_date, end_date)

                # Retrieve results
                main_row                    = future_dashboard_data.result()
                bandwidth_rows              = future_bandwidth_data.result()
                level_rows                  = future_level_data.result()
                traffic_event_rows          = future_traffic_event_data.result()
                server_wise_log_data_rows   = fetch_server_wise_log_data.result()
            # Format data
            formatted_data = self.format_data(main_row, bandwidth_rows, level_rows, traffic_event_rows, server_wise_log_data_rows, start_date, end_date)

            # Return formatted data as JSON response
            return JsonResponse(formatted_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)