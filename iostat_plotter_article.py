#!/usr/bin/python
#
# Simple data plotter for iostat output. Feb. 9, 2013
#
# Copyright Jeffrey B. Layton
#
# License: GNU GPL v2 (http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
# Version 2, June 1991
#
# Copyright (C) 1989, 1991 Free Software Foundation, Inc.  
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
#
#
# To run the application first gather the iostat information using:
#
#  [laytonjb ~]$ iostat -c -d -x -t -m /dev/sda 1 100 > iostat.out
#
# where /dev/sda is the specific device you want to monitor which is
# up to you (in this version you need to use a specific device), "1 100"
# which tells iostat to use "1" second intervals and "100" means to
# gather data for 100 time (or 100 sceonds in this case).
#
# Then to run iostat_plotter, the command is,
#
# [laytonjb ~]$ iostat_plotter.py iostat.out
#
# where "iostat.out" is the output from iostat. The code is written
# in Python (obviously) and uses the shlex, time, os, and matplotlib
# modules.
#
# When iostat_plotter is done it will create a subdirectory "HTML_REPORT"
# that contains the plots and an html file "report.html". Open that
# html file in a browser or word processor and you will see the plots
# and a small write-up about them. Feel free to modify the code but
# please send back changes.
#

import sys

try:
   import shlex                      # Needed for splitting input lines
except ImportError:
   print "Cannot import shlex module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import time;                       # Needed for time conversion function
   time_var = 1
except:
   time_var = 0;
   print "Cannot import shlex module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import matplotlib.pyplot as plt;   # Needed for plots
   matplotlib_var = 1
except:
   matplotlib_var = 0;
   print "Cannot import shlex module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import os                          # Needed for mkdir
except ImportError:
   print "Cannot import os module - this is needed for this application.";
   print "Exiting..."
   sys.exit();



def Plot3(x1, y1, x2, y2, x3, y3, xlabel, ylabel1, ylabel2, ylabel3, 
          d1, d2, d3, filename):
   #
   # Creates 3 vertical subplots with legends and 1 x-axis label at the
   #   the bottom
   #
   # x1 = x-axis data for top plot
   # x2 = x-axis data for middle plot
   # x3 = x-axis data for bottom plot
   # y1 = y-axis data for top plot
   # y2 = y-axis data for middle plot
   # y3 = y-axis data for bottom plot
   # xlabel = x-axis label (only on bottom plot)
   # ylabel1 = label for top y-axis
   # ylabel2 = label for middle y-axis
   # ylabel3 = label for bottom plot
   # d1 = data label for top plot
   # d2 = data label for middle plot
   # d3 = data label for bottom plot
   # filename = name of file for plot output
   #
   
   # Top plot
   ax1 = plt.subplot(311);              # Define top plot using subplot function
   plt.plot(x1,y1, "ro-", label=d1);    # Plot the first data set with a red line wiht "o" as a symbol
   plt.grid();
   plt.xlabel(" ");                     # Don't put an x-axis label since it's the top plot
   plt.ylabel(ylabel1, fontsize=10);    # Use a 10 pt font for y-axis label
   ax1.set_xticklabels([]);             # get x-axis tick label
   leg1 = plt.legend(loc=1);            # Create legend in upper right corner (loc=1)
   frame1 = leg1.get_frame();
   frame1.set_facecolor("0.80");        # Make legend box have a gray background
   for t in leg1.get_texts():
      t.set_fontsize(10);               # Change the font size of the legend text to 10 pt.
   # end for
   
   # Middle plot
   ax2 = plt.subplot(312);
   plt.plot(x2,y2, "bo-", label=d2);
   plt.grid();
   plt.xlabel(" ");
   plt.ylabel(ylabel2, fontsize=10);
   ax2.set_xticklabels([]);
   leg2 = plt.legend(loc=1);
   frame2 = leg2.get_frame();
   frame2.set_facecolor("0.80");
   for t in leg2.get_texts():
      t.set_fontsize(10);
   # end for
   
   # Bottom plot
   plt.subplot(313);
   plt.plot(x3,y3, "go-", label=d3);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel3, fontsize=10);
   leg3 = plt.legend(loc=1);
   frame3 = leg3.get_frame();
   frame3.set_facecolor("0.80");
   for t in leg3.get_texts():
      t.set_fontsize(10);
   # end for
   
   # Either save the plot to a file or display it to the screen
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def



def Plot2(x1, y1, x2, y2, xlabel, ylabel1, ylabel2, d1, d2, filename):
   #
   # Creates 2 vertical subplots with legends and 1 x-axis label at the
   #   the bottom
   #
   # x1 = x-axis data for top plot
   # x2 = x-axis data for bottom plot
   # y1 = y-axis data for top plot
   # y2 = y-axis data for bottom plot
   # xlabel = x-axis label (only on bottom plot)
   # ylabel1 = label for top y-axis
   # ylabel2 = label for bottom y-axis
   # d1 = data label for top plot
   # d2 = data label for bottom plot
   # filename = name of file for plot output
   #
   
   # Top plot
   ax1 = plt.subplot(211);
   plt.plot(x1,y1, "ro-", label=d1);
   plt.grid();
   plt.xlabel(" ");
   plt.ylabel(ylabel1, fontsize=10);
   ax1.set_xticklabels([]);
   leg1 = plt.legend(loc=1);
   frame1 = leg1.get_frame();
   frame1.set_facecolor("0.80");
   for t in leg1.get_texts():
      t.set_fontsize(10);
   # end for
   
   # Bottom Plot
   plt.subplot(212);
   plt.plot(x2,y2, "go-", label=d2);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel2, fontsize=10);
   leg2 = plt.legend(loc=1);
   frame2 = leg2.get_frame();
   frame2.set_facecolor("0.80");
   for t in leg2.get_texts():
      t.set_fontsize(10);
   # end for
   
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def



def Plot1(x, y, xlabel, ylabel, d, filename):
   #
   # Creates 1 chart with a legend and 1 x-axis label
   #
   # x = x-axis data
   # y = y-axis data
   # xlabel = x-axis label
   # ylabel1 = label for y-axis
   # d = data label
   # filename = name of file for plot output
   #
   
   plt.plot(x,y, "go-", label=d);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel, fontsize=10);
   leg = plt.legend(loc=1);
   frame = leg.get_frame();
   frame.set_facecolor("0.80");
   for t in leg.get_texts():
      t.set_fontsize(10);
   # end for
   
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def



# ===================
# Main Python section
# ===================

if __name__ == '__main__':

   print "iostat plotting script";
   input_filename = sys.argv[1];  # Get input file
   print " ";
   print "input filename: ",input_filename;
   
   # Initialize lists that will store data
   user_list = [];
   nice_list = [];
   system_list = [];
   iowait_list = [];
   steal_list = [];
   idle_list = [];
   rrqm_list = [];
   wrqm_list = [];
   r_list = [];
   w_list = [];
   rMB_list = [];
   wMB_list = [];
   avgrqsz_list = [];
   avgqusz_list = [];
   await_list = [];
   r_await_list = [];
   w_await_list = [];
   svctm_list = [];
   util_list = [];
   date_list = [];
   time_list = [];
   meridian_list = [];
   
   # flags for controlling flow
   info_flag = 0;       # 0 = gather system data, 1 = don't gather system data
   cpu_flag = -1;       # -1 = store CPU header info (only done once), 1 = store values, 2 = done
   device_flag = -1;    # -1 = store Device header info (only done once), 1 = store values, 2 = done
   data_flag = 0;       # -1 = cpu, 1 = device (which set of data is being gathered)
   
   # loop over lines in input file
   print " ";
   print "reading iostat output file ... ";
   icount = 0;
   for line in open(input_filename,'r').readlines():
      currentline = shlex.split(line);
      
      if (info_flag == 0):
         system_info = {};
         system_info["OS"] = currentline[0];
         system_info["kernel"] = currentline[1];
         system_info["system_name"] = currentline[2][1:len(currentline[2])-1];
         system_info["date"] = currentline[3];
         system_info["CPU"] = currentline[4];
         system_info["cores"] = currentline[5][1:];
         info_flag = 1;
      # end if
      
      if (len(currentline) > 0):
         if (currentline[0] == "avg-cpu:"): 
            data_flag = -1;
            date_list.append(old_currentline[0].replace("/"," "));
            # if meridian is PM then need to add 12 hours to time_list
            if (old_currentline[2] == "PM"):
               junk1 = old_currentline[1].replace(":"," ");
               junk2 = shlex.split(junk1);
               junk3 = int(junk2[0]) + 12;
               junk4 = str(junk3) + ":" + junk2[1] + ":" + junk2[2];
               time_list.append(junk4);
            else:
               time_list.append(old_currentline[1]);
            # end if
            meridian_list.append(old_currentline[2]);
         elif (currentline[0] == "Device:"):
            data_flag = 1;
         # end if
         if (data_flag == -1):
            if (cpu_flag == -1):
               #print "      Storing CPU headers";
               cpu_labels = [];
               cpu_labels = currentline;
	       cpu_flag = 1;
            elif (cpu_flag == 1):
               #print "      Storing CPU values";
               user_list.append(float(currentline[0]));
               nice_list.append(float(currentline[1]));
               system_list.append(float(currentline[2]));
               iowait_list.append(float(currentline[3]));
               steal_list.append(float(currentline[4]));
               idle_list.append(float(currentline[5]));
               cpu_flag = 2;
               data_flag = 0;
            elif (cpu_flag == 2):
               #print "      CPU header found - getting ready to read CPU data";
               cpu_flag = 1;
            else:
               print "Problem - weird value of cpu_flag: ",cpu_flag," stopping";
               sys.exit();
            # end if
         elif (data_flag == 1):
            if (device_flag == -1):
               #print "      Storing Device headers";
               device_labels = [];
               device_labels = currentline;
               device_flag = 1;
            elif (device_flag == 1):
               #print "      Storing Device values";
               rrqm_list.append(float(currentline[1]));
               wrqm_list.append(float(currentline[2]));
               r_list.append(float(currentline[3])); 
               w_list.append(float(currentline[4]));
               rMB_list.append(float(currentline[5]));
               wMB_list.append(float(currentline[6]));
               avgrqsz_list.append(float(currentline[7]));
               avgqusz_list.append(float(currentline[8]));
               await_list.append(float(currentline[9]));
               r_await_list.append(float(currentline[10]));
               w_await_list.append(float(currentline[11]));
               svctm_list.append(float(currentline[12]));
               util_list.append(float(currentline[13]));
               device_flag = 2;
               data_flag = 0;
               icount = icount + 1;
            elif (device_flag == 2):
               #print "      Device header - getting ready to read device data";
               device_flag = 1;
            else:
               print "Problem - weird value of device_flag: ",device_flag," stopping";
               sys.exit();
            # end if
         # end if
      # end if
      old_currentline = currentline;  # storing Old line so time stamp data can be stored
   # end for
   print "Finished reading ",icount," data points. Creating plots and HTML report";
   
   # Create time list for x-axis data (need to convert to regular time format)
   x_seconds = [];
   for i in range(0,len(date_list)):
      test2 = shlex.split(date_list[i]);
      test3 = test2[2] + "-" + test2[0] + "-" + test2[1];
      
      junk1 = test3 + " " + time_list[i];
      ts = time.mktime(time.strptime(junk1, '%Y-%m-%d %H:%M:%S'));
      if (i == 0):
         BeginTime = ts;
         x_seconds.append(0.0);
      else:
         x_seconds.append( (ts - BeginTime) );
      # end if
   # end of
   
   # "Total" CPU utilziation (user + system)
   time_sum_list = [];
   for i in range(0,len(user_list)):
       time_sum_list.append( (user_list[i] + system_list[i]) );
   # end for
   
   # 
   # HTML Report initialization
   #    Write all data files to subdirectory called HTML_REPORT
   #    File is report.html
   dirname ="./HTML_REPORT";
   if not os.path.exists(dirname):
      os.makedirs(dirname);
   # end if
   html_filename = dirname + '/report.html';
   f = open(html_filename, 'w')
   
   # Print HTML Report header
   output_str = "<H2>\n";
   output_str = output_str + "IOSTAT Report for file: " + input_filename + " \n";
   output_str = output_str + "</H2>\n";
   output_str = output_str + " \n";
   
   # HTML Introduction
   output_str = "<H3>\n";
   output_str = output_str + "Introduction \n";
   output_str = output_str + "</H3> \n \n";
   output_str = output_str + "<P>\n";
   output_str = output_str + "This report plots the iostat output contained in file: \n";
   output_str = output_str + sys.argv[1] + ". It contains a series of plots of the output \n";
   output_str = output_str + "from iostat that was captured. The report is contained in a\n";
   output_str = output_str + "subdirectory HTML_REPORT. In that directory you will find a \n";
   output_str = output_str + "file name report.html. Just open that file in a browser \n";
   output_str = output_str + "and you will see the plots. Please note that all plots are \n";
   output_str = output_str + "referenced to the beginning time of the iostat run. \n";
   output_str = output_str + "</P>\n";
   output_str = output_str + " \n";
   f.write(output_str);
   
   # HTML System Output (from iostat):
   output_str = "<P> \n";
   output_str = output_str + "IOstat outputs a number of basic system parameters when it \n";
   output_str = output_str + "creates the output. These parameters are listed below. \n";
   output_str = output_str + "<UL> \n";
   output_str = output_str + "   <LI>System Name: " + system_info["system_name"] + " \n";
   output_str = output_str + "   <LI>OS: " + system_info["OS"] + " \n";
   output_str = output_str + "   <LI>Kernel: " + system_info["kernel"] + " \n";
   output_str = output_str + "   <LI>Number of Cores " + system_info["cores"] + " \n";
   output_str = output_str + "   <LI>Core Type " + system_info["CPU"] + " \n";
   output_str = output_str + "</UL> \n";
   output_str = output_str + "The iostat run was started on " + system_info["date"] + " at \n";
   output_str = output_str + time_list[0] + " " + meridian_list[0] + ". \n";
   output_str = output_str + "</P> \n";
   f.write(output_str);
   
   # HTML hyperlinks
   output_str = "<P> \n";
   output_str = output_str + "Below are hyperlinks to various plots within the report. \n";
   output_str = output_str + "<BR> \n";
   output_str = output_str + "<OL> \n";
   output_str = output_str + "   <LI><a href=\"#cpu_utilization\">CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#iowait_cpu_utilization\">IOwait Percentage Time</a> \n";
   output_str = output_str + "   <LI><a href=\"#steal_cpu_utilization\">Steal Percentage Time</a> \n";
   output_str = output_str + "   <LI><a href=\"#idle_cpu_utilization\">Idle Percentage Time</a> \n";
   output_str = output_str + "   <LI><a href=\"#rmb_total_cpu\">Read Throughput and Total CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#wmb_total_cpu\">Write Throughput and Total CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#requests_complete_total_cpu\">Read Requests Complete Rate, Write Requests Complete Rate, and Total CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#requests_merged_total_cpu\">Read Requests Merged Rate, Write Requests Merged Rate, and Total CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#requests_queue_total_cpu\">Average Request Size, Average Queue Length, and Total CPU Utilization Percentage</a> \n";
   output_str = output_str + "   <LI><a href=\"#avg_wait_time_total_cpu\">Average Read Request Time, Average Write Request Time, and Total CPU Utilization</a> \n";
   output_str = output_str + "   <LI><a href=\"#util_cpu_total_cpu\">Percentage CPU Time for IO Requests and Total CPU Utilization</a> \n";
   output_str = output_str + "</OL> \n";
   output_str = output_str + "</P> \n";
   output_str = output_str + " \n";
   f.write(output_str);
   
   # Figure 1: Various CPU percentages (user, system, nice) vs. time (3 subplots)
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "1. <a id=\"cpu_utilization\">Percentage CPU Time (CPU Utilization)</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure plots three types of CPU Utilization: (1) User, \n";
   output_str = output_str + "(2) System, and (3) Nice. The User utilization is the  percentage \n";
   output_str = output_str + "of CPU utilization that occurred while executing at the user level \n";
   output_str = output_str + "(applications).The System utilization is the percentage of CPU \n";
   output_str = output_str + "utilization that occurred while executing at the system level \n";
   output_str = output_str + "(kernel). The third time is the Nice utilization which is the \n";
   output_str = output_str + "percentage of CPU utilization that occurred while executing at \n";
   output_str = output_str + "the  user  level with nice priority. \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "% CPU Utilization \n by User tasks";
   ylabel2 = "% CPU Utilization \n by System tasks";
   ylabel3 = "% CPU Utilization \n by Nice tasks";
   xlabel = "Time (seconds)";
   d1 = "User";
   d2 = "System";
   d3 = "Nice";
   filename = dirname + "/percentage_cpu_utilization";
   Plot3(x_seconds, user_list, x_seconds, system_list, x_seconds, nice_list,
         xlabel, ylabel1, ylabel2, ylabel3, d1, d2, d3, filename);
   # HTML Output: (Figure html)
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"percentage_cpu_utilization.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 1 - Percentage CPU Utilization (User, System, and Nice)</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 1 of 11";
   
   # Figure 2: iowait percentage time
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "2. <a id=\"iowait_cpu_utilization\">IOWait Percentage Time</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This is the percentage of time that the CPU or CPUs were idle \n";
   output_str = output_str + "during which the system had an outstanding disk device I/O request. \n";
   f.write(output_str);
   
   # make the plot
   ylabel = "% IOwait CPU Percentage Time \n Waiting for IO requests";
   xlabel = "Time (seconds)";
   d = "IOwait";
   filename = dirname + "/iowait_percentage_cpu_time";
   #filename ="";
   Plot1(x_seconds, iowait_list, xlabel, ylabel, d, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"iowait_percentage_cpu_time.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 2 - Percentage CPU Time waiting to process disk requests</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 2 of 11";

   # Figure 3: Steal Time
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "3. <a id=\"steal_cpu_utilization\">Steal Percentage Time</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This is the percentage of time spent in involuntary \n";
   output_str = output_str + "wait by the virtual CPU or CPUs while the hypervisor was \n";
   output_str = output_str + "servicing another virtual processor. \n";
   f.write(output_str);
   
   # make the plot
   ylabel = "% Steal CPU Percentage Time \n Waiting for IO requests";
   xlabel = "Time (seconds)";
   d = "Steal";
   filename = dirname + "/steal_percentage_cpu_time";
   #filename ="";
   Plot1(x_seconds, steal_list, xlabel, ylabel, d, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"steal_percentage_cpu_time.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 3 - Percentage CPU Time in involuntary waiting</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 3 of 11";
   
   # Figure 4: Idle Time
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "4. <a id=\"idle_cpu_utilization\">Idle Percentage Time with no IO requests</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This is the percentage of time that the CPU or CPUs were \n";
   output_str = output_str + "idle and the system did not have an outstanding disk I/O request. \n";
   f.write(output_str);
   
   # make the plot
   ylabel = "% Idle CPU Percentage Time \n and no Waiting for IO requests";
   xlabel = "Time (seconds)";
   d = "Idle";
   filename = dirname + "/idle_percentage_cpu_time";
   #filename ="";
   Plot1(x_seconds, idle_list, xlabel, ylabel, d, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"idle_percentage_cpu_time.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 4 - Percentage CPU Time in idle activities with no IO requests</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 4 of 11";
   
   # Figure 5: Read Throughput and Total CPU Utilization
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "5. <a id=\"rmb_total_cpu\">Read Throughput and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has two parts. The top graph plots the Read Rate \n";
   output_str = output_str + "in MB/s versus time and the bottom graph plots the Total CPU \n";
   output_str = output_str + "Utilization percentage (User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Read Throughput (MB/s)";
   ylabel2 = "Total CPU Percentage Utilization";
   xlabel = "Time (seconds)";
   d1 = "Read Throughput";
   d2 = "Total CPU Utilization";
   filename = dirname + "/read_throughput";
   #filename ="";
   Plot2(x_seconds, rMB_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, d1, d2, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"read_throughput.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 5 - Read Throughput (MB/s) and Total CPU Utilization Percentage</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 5 of 11";
   
   # Figure 6: Write Throughput and Total CPU Utilization
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "6. <a id=\"wmb_total_cpu\">Write Throughput and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has two parts. The top graph plots the Write Rate \n";
   output_str = output_str + "in MB/s versus time and the bottom graph plots the Total CPU \n";
   output_str = output_str + "Utilization percentage (User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Write Throughput (MB/s)";
   ylabel2 = "Total CPU Percentage Utilization";
   xlabel = "Time (seconds)";
   d1 = "Write Throughput";
   d2 = "Total CPU Utilization";
   filename = dirname + "/write_throughput";
   #filename ="";
   Plot2(x_seconds, wMB_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, d1, d2, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"write_throughput.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 6 - Write Throughput (MB/s) and Total CPU Utilization Percentage</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 6 of 11";

   # Figure 7: Read Request complete rate, Write Request complete rate, and Total CPU Utilization
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "7. <a id=\"requests_complete_total_cpu\">Read Requests Complete, Write Requests Complete, and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has three parts. The top graph plots the number (after \n";
   output_str = output_str + "merges) of read requests completed per second for the device \n";
   output_str = output_str + "versus time. The middle graph plots the number (after merges) \n";
   output_str = output_str + "of write requests completed per second for the device versus time. \n";
   output_str = output_str + "The bottom graph plots the Total CPU Utilization percentage \n";
   output_str = output_str + "(User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Read requests \n complete rate \n (requests/s)";
   ylabel2 = "Write requests \n complete rate \n (requests/s)";
   ylabel3 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Read requests complete";
   d2 = "Write requests complete";
   d3 = "Total CPU Utilization";
   filename = dirname + "/read_write_requests_complete_rate";
   #filename ="";
   Plot3(x_seconds, r_list, x_seconds, w_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, ylabel3, d1, d2, d3, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"read_write_requests_complete_rate.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 7 - Read Requests Completed Rate (requests/s), Write Requests Completed Rate (requests/s), and Total CPU Utilization Percentage</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 7 of 11";
   
   # Figure 8: Read Request merge rate, Write Request merge rate, and Total CPU Utilization
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "8. <a id=\"requests_merged_total_cpu\">Read Requests Merged rate, Write Requests Merged rate, and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has three parts. The top graph plots the number \n";
   output_str = output_str + "of read requests merged per second that were queued to the device. \n";
   output_str = output_str + "The middle graph plots the number of write requests merged per \n";
   output_str = output_str + "second that were queued to the device. The bottom graph plots \n";
   output_str = output_str + "the Total CPU Utilization percentage (User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Read request \n merged rate \n (requests/s)";
   ylabel2 = "Write request \n merged rate \n (requests/s)";
   ylabel3 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Read requests merged";
   d2 = "Write requests merged";
   d3 = "Total CPU Utilization";
   filename = dirname + "/read_write_requests_merged_rate";
   #filename ="";
   Plot3(x_seconds, rrqm_list, x_seconds, wrqm_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, ylabel3, d1, d2, d3, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"read_write_requests_merged_rate.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 8 - Read Requests Merged Rate (requests/s), Write Requests Merged Rate (requests/s), and Total CPU Utilization Percentage</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 8 of 11";
   
   # Figure 9: Read Request merge rate, Write Request merge rate, and Total CPU Utilization
   # HTML report output (opt of section)
   output_str = "<H4> \n"
   output_str = output_str + "9. <a id=\"requests_queue_total_cpu\">Average Request Size, Average Queue Length, and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has three parts. The top graph plots the average \n";
   output_str = output_str + "size (in sectors) of the requests that were issued to the \n";
   output_str = output_str + "device. The middle graph plots the average queue length of \n";
   output_str = output_str + "the requests that were issued to the device. The bottom graph \n";
   output_str = output_str + "plots the Total CPU Utilization percentage (User Time + System \n";
   output_str = output_str + "Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Average Size of \n IO requests \n (sectors)";
   ylabel2 = "Average Queue length \n of requests ";
   ylabel3 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Avg. Request Size";
   d2 = "Avg. Queue length";
   d3 = "Total CPU Utilization";
   filename = dirname + "/requests_queue_total_cpu";
   #filename ="";
   Plot3(x_seconds, rrqm_list, x_seconds, wrqm_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, ylabel3, d1, d2, d3, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"requests_queue_total_cpu.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 9 - Average Request Size (sectors), Average Queue Length, and Total CPU Utilization Percentage</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 9 of 11";
   
   # Figure 10: Average Wait Times for read, write requests
   # HTML report output (top of section)
   output_str = "<H4> \n"
   output_str = output_str + "10. <a id=\"avg_wait_time_total_cpu\">Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has three parts. The top graph plots the average \n";
   output_str = output_str + "time (in milliseconds) for read requests issued to \n";
   output_str = output_str + "the device to be served. This includes the time spent by the \n";
   output_str = output_str + "requests in queue and the time spent servicing them. The middle \n";
   output_str = output_str + "graph plots the average time (in milliseconds) for write \n";
   output_str = output_str + "requests issued to the device to be  served. This includes \n";
   output_str = output_str + "the time spent by the requests in queue and the time spent \n";
   output_str = output_str + "servicing them. The bottom graph plots the Total CPU Utilization \n";
   output_str = output_str + "percentage (User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Average Read Request \n Time (ms)";
   ylabel2 = "Average Write Request \n Time (ms)";
   ylabel3 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Avg. Read Request Time";
   d2 = "Avg. Write Request Time";
   d3 = "Total CPU Utilization";
   filename = dirname + "/avg_request_time_total_cpu";
   #filename ="";
   Plot3(x_seconds, r_await_list, x_seconds, w_await_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, ylabel3, d1, d2, d3, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"avg_request_time_total_cpu.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 10 - Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 10 of 11";
   
   # Figure 11: Percentage CPU Util
   # HTML report output (top of section)
   output_str = "<H4> \n"
   output_str = output_str + "11. <a id=\"util_cpu_total_cpu\">Percentage CPU Time for IO Requests and Total CPU Utilization</a> \n";
   output_str = output_str + "</H4> \n";
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has two parts. The top graph plots the \n";
   output_str = output_str + "percentage of CPU time during which I/O requests were issued \n";
   output_str = output_str + "to the device (bandwidth utilization for the device). \n";
   output_str = output_str + "Device saturation occurs when this value is close to 100%. \n";
   output_str = output_str + "The bottom graph plots the Total CPU Utilization percentage \n";
   output_str = output_str + "(User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "% CPU time for IO \n Requests";
   ylabel2 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Util";
   d2 = "Total CPU Utilization";
   filename = dirname + "/util_cpu_total_cp";
   #filename ="";
   Plot2(x_seconds, util_list, x_seconds, time_sum_list, xlabel, ylabel1, 
         ylabel2, d1, d2, filename);
   # HTML Output:
   output_str = "<center> \n";
   output_str = output_str + "<img src=\"util_cpu_total_cp.png\"> \n";
   output_str = output_str + "<BR><BR><strong>Figure 11 - Percentage CPU Time for IO Requests and Total CPU Utilization</strong></center><BR><BR> \n";
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   print "   Finished Plot 11 of 11";
   print "Finished. Please open the document HTML/report.html in a browser.";
   
# end
