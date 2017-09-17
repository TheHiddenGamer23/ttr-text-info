import os
import glob
import time


#DIR = 'C:/Program Files (x86)/Toontown Rewritten/logs' # for windows, "c:/Program Files (x86)/Toontown Rewritten/logs" should be default. linux: '/path/to/ttr/files/logs' is where you need


class ReadLog:

    def __init__(self, logdir):
        self.logdir = logdir
        self.update_file()
        self.dists = {
            "504": "Blam Canyon",
            "511": "Boingbury",
            "510": "Bounceboro",
            "502": "Fizzlefield",
            "500": "Gulp Gulch",
            "505": "Hiccup Hills",
            "509": "Kaboom Cliffs",
            "501": "Splashport",
            "506": "Splat Summit",
            "507": "Thwackville",
            "503": "Woosh Rapids",
            "508": "Zoink Falls"
        }
        self.knowndist = None



    def update_file(self):
        #print('updating logfile...')
        list_of_files = glob.glob(self.logdir + '/*.log') # * means all if need specific format then *.csv
        self.latest_file = max(list_of_files, key=os.path.getctime)
        self.filechecktime = time.time()

    def tail(self, f, lines=20 ): #thanks to S. Lott at stackoverflow: https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
        total_lines_wanted = lines

        BLOCK_SIZE = 1024
        f.seek(0, 2)
        block_end_byte = f.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                    # from the end of the file
        while lines_to_go > 0 and block_end_byte > 0:
            if (block_end_byte - BLOCK_SIZE > 0):
                # read the last block we haven't yet read
                f.seek(block_number*BLOCK_SIZE, 2)
                blocks.append(f.read(BLOCK_SIZE))
            else:
                # file too small, start from begining
                f.seek(0,0)
                # only read what was not read
                blocks.append(f.read(block_end_byte))
            lines_found = blocks[-1].count(b'\n')
            lines_to_go -= lines_found
            block_end_byte -= BLOCK_SIZE
            block_number -= 1
        for i, blk in enumerate(blocks):
            blocks[i] = str(blk)
        #print(blocks)
        all_read_text = ''.join(reversed(blocks)).replace('\'b"', '')
        #print(all_read_text)
        return all_read_text.split("\\r\\n")[-total_lines_wanted:]


    def findlastdist(self):
        with open(self.latest_file, 'br') as file:
            lastdistfound = None
            lines = self.tail(file, 100)
        #print(lines)
        for i in lines:
            if i.startswith(':OTPClientRepository: Entering shard'):
                lastdistfound = i.split()[3][:3]
        if lastdistfound != None:
            return lastdistfound.strip()


    def run(self):
        #print('running')
        if self.filechecktime + 60 < time.time():
            self.update_file()
        dist = self.findlastdist()
        if dist == None:
            pass
        elif self.knowndist != dist:
            self.knowndist = dist
            return self.dists[dist[:3]]
def main():
    if os.path.exists('config.ini') and os.path.isfile('config.ini'):
        with open('config.ini') as ini:
            inidir = ini.readline().strip()
        if os.path.exists(inidir) and not os.path.isfile(inidir):
            DIR = inidir
            print('Assuming newest file in %s\n is the newest log file from Toontown Rewritten, correct the directory in\n \'config.ini\' if this is incorrect!' % inidir)
        else:
            print('file \'config.ini\' contains invalid value: line one should contain a path to the Toontown Rewritten \'logs\' folder.')
            if os.name == 'nt':
                os.system("pause")
            else:
                os.system('read -s -n 1 -p "Press any key to continue..."')
            return
    else:
        
        try:
            PROGRAMSX86 = os.environ.get('PROGRAMFILES(X86)')
            DIR = PROGRAMSX86 + '\\Toontown Rewritten\\logs'
        except:
            with open('config.ini', 'w') as ini: #Fallback in case this isn't windows.
               ini.write('/dir/goes/here/ToontownRewritten/logs')
            print('config.ini created.')
        else:
            if os.path.exists(DIR):
                print('Assuming default installation location: '+ DIR)
                print('if this is incorrect, change the contents of the file config.ini to the correct directory!')
                with open('config.ini', 'w') as ini:
                    ini.write(DIR)
            else:
                print('unknown Toontown Rewritten file location, creating \'config.ini\' file within this directory, please input the Toontown Rewritten files directory in it as it showsin the file.')
                with open('config.ini', 'w') as ini:
                    ini.write(DIR)
        if os.name == 'nt':
            os.system("pause")
        else:
            os.system('read -s -n 1 -p "Press any key to continue..."')
        return
        
        
    logread = ReadLog(DIR)
    print('starting output to: district.txt')
    while True:
        dist = logread.run()
        if dist != None:
            print('found new dist: ', dist)
            with open('district.txt', 'w') as f:
                f.write(dist)
        time.sleep(5)
main()