import utime

class Logger:
    def __init__(self):
        self.file = open ("logging.txt", "w")
        self.file.close()        
    
    def log(self, error):
        
        current_time = utime.time()
        formatted_time = utime.localtime(current_time)
        output_string = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            formatted_time[0], formatted_time[1], formatted_time[2],
            formatted_time[3], formatted_time[4], formatted_time[5]
        )

        with open("logging.txt", "a") as file:
            file.write("\n " + output_string + "| ")
            file.write(error)
            print(error)

    def log_with_out_print(self, error):
        
        current_time = utime.time()
        formatted_time = utime.localtime(current_time)
        output_string = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            formatted_time[0], formatted_time[1], formatted_time[2],
            formatted_time[3], formatted_time[4], formatted_time[5]
        )

        with open("logging.txt", "a") as file:
            file.write("\n " + output_string + "| ")
            file.write(error)

