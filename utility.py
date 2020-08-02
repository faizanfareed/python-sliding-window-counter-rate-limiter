
import datetime


class Utility:

    def print_logs(self, result):
        '''Print eeach log in user log.'''

        if self.is_log_enabled: 
            if self.is_ratelimit_reset_header_allowed: 
                logs = result[6] 
                self.count_logs(logs)  
            else:  
                logs = result[4]  
                self.count_logs(logs) 

    def count_logs(self, logs):

        ''''Count expired and valid logs in rate limit time window.'''

        logCount = 0
        logExpiredCount = 0

        t = datetime.datetime.fromtimestamp(self.slidingTimeWindow)

        t = datetime.datetime.strftime(
            t, self.fixed_time_window_format_for_insertion)

        print('Logs  Sliding Time ', t, ' - ', self.request_recieved_at)

        for log in logs:
            t = int(log.decode())
            times = datetime.datetime.fromtimestamp(t)
            times = times.strftime("%H:%M:%S")

            print(times, end=" | ")

        for log in logs:
            if int(log.decode()) < self.slidingTimeWindow:
                #print('Log key Deleted : ', int(log.decode()))
                logExpiredCount = logExpiredCount + 1
            else:
                #print('Log key : ',int(log.decode()) )
                logCount = logCount + 1
       
        print('Log inlcuded : ', logCount)

        print('Log not included : ', logExpiredCount)

    
        print('Included  windows : ', self.total_request_served)

        print('Not Inlcuded windows : ', self.total_expired_time_windows)


    def print_all_timewindows(self, time_window_list):

        '''Print and count expired and valid windows in rate limit time window.'''
        
        print('Windows Included')

        for window, counts in time_window_list.items():
            if int(window.decode()) < self.slidingTimeWindow:
                pass
            else:
                t = int(window.decode())
                times = datetime.datetime.fromtimestamp(t)
                times = times.strftime("%H:%M:%S")

                print(times, end=" | ")

        print('\nWindows Not Included')
        for window, counts in time_window_list.items():

            if int(window.decode()) < self.slidingTimeWindow:

                t = int(window.decode())
                times = datetime.datetime.fromtimestamp(t)
                times = times.strftime("%H:%M:%S")

                print(times, end=" | ")
            else:
                pass

        print('\n')
        print('Sliding Window Time : ', self.slidingTimeWindow)

        print('All windows  \n')

        for window, counts in time_window_list.items():

            t = int(window.decode())

            print(t, ':', int(counts.decode()), end=" | ")

        print('\n')

    
  

    def getRequestInsertionTimeStr(self):
        '''Return request time in str format.'''

        if self.request_recieved_at:
            return self.request_recieved_at.strftime("%Y:%m:%d:%H:%M:%S:%M")

    

    def getCurrentUnixtimestamp(self):
        '''get current timestamp for request'''

        t = datetime.datetime.now()
        return int(datetime.datetime.timestamp(t))

    def insertLogrequest(self):
        '''Insert each requrest into log'''

        if self.is_log_enabled:  

            self.pipeline.execute_command(
                'ZADD', 'log:'+self.clientid, 'nx', 1, self.getCurrentUnixtimestamp())
            self.pipeline.execute_command(
                'ZRANGE', 'log:'+self.clientid, 0, -1)
            self.pipeline.execute_command(
                'EXPIRE', 'log:'+self.clientid, self.expiration_time_of_client_keys)
