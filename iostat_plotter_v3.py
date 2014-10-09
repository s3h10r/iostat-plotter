#!/usr/bin/python
#
# Enhanced data plotter for iostat output. Feb. 22 2014
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
# [laytonjb ~]$ iostat -c -d -x -t -m /dev/sda 1 100 > iostat.out
#
# where /dev/sda is the specific device you want to monitor which is
# up to you. If you don't put a device there, iostat will monitor
# all devices. For example:
#
# [laytonjb ~]$ iostat -c -d -x -t -m 1 100 > iostat.out
#
# "1 100" which tells iostat to use "1" second intervals  and "100" 
# means to gather data for 100 time (or 100 sceonds in this case).
#
# Then to run iostat_plotter, the command is,
#
# [laytonjb ~]$ iostat_plotter.py iostat.out
#
# where "iostat.out" is the output from iostat. The code is written
# in Python (obviously) and uses the shlex, time, os, and matplotlib
# modules. iostat_plotter is smart enough to gather the data for each
# device and plot them separately.
#
# Alternatively, you can run iostat_plotter.py as,
#
# [laytonjb ~]$ iostat_plotter.py -c iostat.out
#
# where the option "-c" stands for "combined" plots which plots all
# of the devices on the same plot.
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
   print "Cannot find time module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import matplotlib.pyplot as plt;   # Needed for plots
   matplotlib_var = 1
except:
   matplotlib_var = 0;
   print "Cannot find matplotlib - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import os                           # Needed for mkdir
except ImportError:
   print "Cannot import os module - this is needed for this application.";
   print "Exiting..."
   sys.exit();

try:
   import pickle                      # Needed for pickle
   pickle_success = 1;
except ImportError:
   print "Cannot import pickle module - this is not needed for this application.";
   print "Continuing to process";
   pickle_success = 0;


# ------------------------------


def help_out():
   # prints out help information and stops
   print " ";
   print "This application creates a short HTML based report from iostat output";
   print "(part of the sysstat tools). The report includes plots that help";
   print "analyze the output. It can adapt to sysstat v9.x format or sysstat";
   print "v10.x output (it is slightly different). Many distributions such as";
   print "CentOS or Red Hat use sysstat version 9.x. However, it is recommended";
   print "that you upgrad to sysstat 10.x because you get slightly more information.";
   print "It is not a difficult task but be sure you install over the previous";
   print "version.";
   print " ";
   print "To run the application first gather the iostat information using: ";
   print "the following example.";
   print " ";
   print "[laytonjb ~]$ iostat -c -d -x -t -m /dev/sda 1 100 > iostat.out ";
   print " ";
   print "where the \"-c\" option displays the CPU utilization, the \"-d\" option";
   print "displays the device utilization, the \"-x\" option displays extended";
   print "statistics, and the \"-m\" option diplays the statistics in megabytes";
   print "per second. The options \"1 100\" tell iostat to use \"1\" second ";
   print "intervals and \"100\" means to gather data for 100 internvals (or 100";
   print "seconds in this case). ";
   print " ";
   print "After the \"-m\" option is /dev/sda which is the specific device";
   print "you want to monitor. This option is up to you. If you don't put a ";
   print "device there, iostat will monitor all devices. For example:"
   print " ";
   print "[laytonjb ~]$ iostat -c -d -x -t -m 1 100 > iostat.out ";
   print " ";
   print "which captures the data from all devices.";
   print " ";
   print "In these two examples, the output from iostat is send to a file which is";
   print "\"iostat.out\". You can name the file anything you want but be sure ";
   print "note the name of the file.";
   print " ";
   print "Then to run iostat_plotter using the iostat output file, the command is, ";
   print " ";
   print "[laytonjb ~]$ iostat_plotter.py iostat.out ";
   print " ";
   print "where \"iostat.out\" is the output from iostat. The code is written ";
   print "in Python (obviously) and uses the shlex, time, os, and matplotlib ";
   print "modules. Be sure this libraries are installed on your system.";
   print " ";
   print "You can run iostat_plotter in one of two ways. The first way creates ";
   print "the set of plots for each device on the node. In this version of ";
   print "iostat_plotter, 11 plots are created per device, so if you have two";
   print "devices on the node, then you will ahve a total of 22 plots.";
   print " ";
   print "The other way to run niostat_plotter is to combine the results for each";
   print "device in the plots. This means you will have only 11 plots ";
   print "in the HTML report even if you have more than one device. You run this ";
   print "with the following command:";
   print " ";
   print "[laytonjb ~]$ iostat_plotter.py -c iostat.out ";
   print " ";
   print "The option \"-c\" tells iostat_plotter to \"combine\" the results from";
   print "all of the devices into a single plot. Currently, you can analyze about";
   print "8 devices. With more than 8 devices, the legend labels run into each other.";
   print " ";
   print "When iostat_plotter is done it will create a subdirectory \"HTML_REPORT\" ";
   print "that contains the plots and an html file \"report.html\". Open that ";
   print "html file in a browser or word processor and you will see the plots ";
   print "and a small write-up about them. Feel free to modify the code but ";
   print "please send back changes. ";
   print " ";

# end def



def Three_Chart(x1, y1, x2, y2, x3, y3, xlabel, ylabel1, ylabel2, ylabel3, 
                d1, d2, d3, fsize, flegsize, filename, box_expansion):
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
   # fsize = font size for tick labels
   # flegsize = font size for legend labels
   # filename = name of file for plot output
   # box_expansion = expansion factor on legend box
   #
   
   # Top plot
   ax1 = plt.subplot(311);                 # Define top plot using subplot function
   plt.plot(x1,y1, "ro-", label=d1);       # Plot the first data set with a red line wiht "o" as a symbol
   plt.grid();
   plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
   plt.ylabel(ylabel1, fontsize=6);    # Use a 10 pt font for y-axis label
   ax1.set_xticklabels([]);                # get x-axis tick label
   
   # Legend
   box = ax1.get_position()
   ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])  
   leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame1 = leg1.get_frame();
   frame1.set_facecolor("0.80");           # Make legend box have a gray background
   for t in leg1.get_texts():
      t.set_fontsize(flegsize);               # Change the font size of the legend text to 10 pt.
   # end for
   
   plt.xticks(fontsize=6);
   plt.yticks(fontsize=6);
   
   # Middle plot
   ax2 = plt.subplot(312);
   plt.plot(x2,y2, "bo-", label=d2);
   plt.grid();
   plt.xlabel(" ");
   plt.ylabel(ylabel2, fontsize=fsize);
   ax2.set_xticklabels([]);
   
   # Legend
   box = ax2.get_position();
   ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height]);
   leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame2 = leg2.get_frame();
   frame2.set_facecolor("0.80");
   for t in leg2.get_texts():
      t.set_fontsize(flegsize);
   # end for
   
   plt.xticks(fontsize=fsize);
   plt.yticks(fontsize=fsize);
   
   # Bottom plot
   ax3 = plt.subplot(313);
   plt.plot(x3,y3, "go-", label=d3);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel3, fontsize=fsize);
   
   # Legend
   box = ax3.get_position()
   ax3.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
   leg3 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame3 = leg3.get_frame();
   frame3.set_facecolor("0.80");
   for t in leg3.get_texts():
      t.set_fontsize(flegsize);
   # end for
   
   plt.xticks(fontsize=fsize);
   plt.yticks(fontsize=fsize);
   
   # Either save the plot to a file or display it to the screen
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def



def Two_Chart(x1, y1, x2, y2, xlabel, ylabel1, ylabel2, d1, d2, fsize, flegsize,
              filename, box_expansion):
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
   # fsize = font size for tick labels
   # flegsize = font size for legend labels
   # filename = name of file for plot output
   # box_expansion = expansion factor for legend
   #
   
   # Top plot
   ax1 = plt.subplot(211);
   plt.plot(x1,y1, "ro-", label=d1);
   plt.grid();
   plt.xlabel(" ");
   plt.ylabel(ylabel1, fontsize=fsize);
   ax1.set_xticklabels([]);
   
   # Legend
   box = ax1.get_position()
   ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
   leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame1 = leg1.get_frame();
   frame1.set_facecolor("0.80");
   for t in leg1.get_texts():
      t.set_fontsize(flegsize);
   # end for
   
   # Bottom Plot
   ax2 = plt.subplot(212);
   plt.plot(x2,y2, "go-", label=d2);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel2, fontsize=fsize);
   
   # Legend
   box = ax2.get_position()
   ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
   leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame2 = leg2.get_frame();
   frame2.set_facecolor("0.80");
   for t in leg2.get_texts():
      t.set_fontsize(fsize);
   # end for
   
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def



def One_Chart(x, y, xlabel, ylabel, d, fsize, flegsize, filename, box_expansion):
   #
   # Creates 1 chart with a legend and 1 x-axis label
   #
   # x = x-axis data
   # y = y-axis data
   # xlabel = x-axis label
   # ylabel1 = label for y-axis
   # d = data label
   # fsize = Font size for tick marks and labels
   # flegsize = Legend font size
   # filename = name of file for plot output
   # box_expansion = expansion factor for legend
   #
   ax1 = plt.subplot(111);
   plt.plot(x,y, "go-", label=d);
   plt.grid();
   plt.xlabel(xlabel);
   plt.ylabel(ylabel, fontsize=fsize);
   
   # Legend
   box = ax1.get_position()
   ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
   leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                     borderpad=0.15, handletextpad=0.2);
   frame = leg1.get_frame();
   frame.set_facecolor("0.80");
   for t in leg1.get_texts():
      t.set_fontsize(flegsize);
   # end for
   
   if (len(filename) == 0):
      plt.show();
   else:
      plt.savefig(filename);
      plt.close();
   # end if
   
# end def




def plot1(iloop, iplot, combined_plots, f, dirname, x_seconds, user_list, system_list, 
          nice_list, fsize, item):
   #
   # Figure 1: Various CPU percentages (user, system, nice) vs. time (3 subplots)
   #
   junk1 = "cpu_utilization" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n";
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Percentage CPU Time (CPU Utilization)</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n";
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Percentage CPU Time (CPU Utilization)</a>";
      output_str = output_str + "</H3> \n";
   #end if
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
   filename = dirname + "/percentage_cpu_utilization" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   # Compute box_expansion factor:
   box_expansion = 0.95;   # Default
   ilongest = 0;
   if (len(d1) > ilongest):
      ilongest = len(d1);
   # end if
   if (len(d2) > ilongest):
      ilongest = len(d2);
   # end if
   if (len(d3) > ilongest):
      ilongest = len(d3);
   # end if
   junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
   expansion_box = round(junk1,2);
   
   Three_Chart(x_seconds, user_list, x_seconds, system_list, x_seconds, nice_list,
               xlabel, ylabel1, ylabel2, ylabel3, d1, d2, d3, fsize, flegsize,
               filename, box_expansion);
   
   # HTML Output: (Figure html)
   output_str = "<center> \n";
   junk1 = "percentage_cpu_utilization" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Utilization (User, System, and Nice) for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Utilization (User, System, and Nice) for device </strong></center><BR><BR> \n";
   #end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot2(iloop, iplot,  combined_plots, f, dirname, x_seconds, iowait_list, 
          fsize, item):
   #
   # Figure 2: iowait percentage time
   #
   junk1 = "iowait_cpu_utilization" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">IOWait Percentage Time</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif(combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">IOWait Percentage Time</a>";
      output_str = output_str + "</H3> \n";
   # end if
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This is the percentage of time that the CPU or CPUs were idle \n";
   output_str = output_str + "during which the system had an outstanding disk device I/O request. \n";
   f.write(output_str);
   
   # make the plot
   ylabel = "% IOwait CPU Percentage Time \n Waiting for IO requests";
   xlabel = "Time (seconds)";
   d = "IOwait";
   filename = dirname + "/iowait_percentage_cpu_time" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   # Compute box_expansion factor:
   box_expansion = 0.96;
   ilongest = 0;
   if (len(d) > ilongest):
      ilongest = len(d);
   # end if
   junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
   expansion_box = round(junk1,2);
   
   One_Chart(x_seconds, iowait_list, xlabel, ylabel, d, fsize, flegsize, filename, box_expansion);
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "iowait_percentage_cpu_time" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time waiting to process disk requests for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time waiting to process disk requests </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot3(iloop, iplot, combined_plots, f, dirname, x_seconds, steal_list, 
          fsize, item):
   #
   # Figure 3: Steal Time
   #
   junk1 = "steal_cpu_utilization" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Steal Percentage Time</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Steal Percentage Time</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   filename = dirname + "/steal_percentage_cpu_time" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   # Compute box_expansion factor:
   box_expansion = 0.96;
   ilongest = 0;
   if (len(d) > ilongest):
      ilongest = len(d);
   # end if
   junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
   expansion_box = round(junk1,2);
   
   One_Chart(x_seconds, steal_list, xlabel, ylabel, d, fsize, flegsize, filename, box_expansion);
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "steal_percentage_cpu_time" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time in involuntary waiting for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time in involuntary waiting </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot4(iloop, iplot, combined_plots, f, dirname, x_seconds, idle_list,
          fsize, item):
   #
   # Figure 4: Idle Time
   #
   junk1 = "idle_cpu_utilization" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Idle Percentage Time with no IO requests</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif(combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Idle Percentage Time with no IO requests</a>";
      output_str = output_str + "</H3> \n";
   # end if
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This is the percentage of time that the CPU or CPUs were \n";
   output_str = output_str + "idle and the system did not have an outstanding disk I/O request. \n";
   f.write(output_str);
   
   # make the plot
   ylabel = "% Idle CPU Percentage Time \n and no Waiting for IO requests";
   xlabel = "Time (seconds)";
   d = "Idle";
   filename = dirname + "/idle_percentage_cpu_time" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   # Compute box_expansion factor:
   box_expansion = 0.97;
   ilongest = 0;
   if (len(d) > ilongest):
      ilongest = len(d);
   # end if
   junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
   expansion_box = round(junk1,2);
   
   One_Chart(x_seconds, idle_list, xlabel, ylabel, d, fsize, flegsize, filename, box_expansion);
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "idle_percentage_cpu_time" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time in idle activities with no IO requests for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time in idle activities with no IO requests </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
# end if




def plot5(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 5: Read Throughput and Total CPU Utilization
   #
   junk1 = "rmb_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Throughput and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Throughput and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   d2 = "Total CPU Util";
   filename = dirname + "/read_throughput" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.88;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Two_Chart(x_seconds, item["rMB"], x_seconds, time_sum_list, xlabel, ylabel1, 
                ylabel2, d1, d2, fsize, flegsize, filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute expansion_box factor:
      box_expansion = 0.88;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(211);
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["rMB"], marker, label=d11);
         plt.xlabel(" ");
         plt.ylabel(ylabel1, fontsize=fsize);
         ax1.set_xticklabels([]); 
      # end for
      plt.grid();
      # Legend
      box = ax1.get_position();
      ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height]);
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      # Bottom Plot
      fsize = 8;
      flegsize = 6;
      ax2 = plt.subplot(212);
      plt.plot(x_seconds, time_sum_list, "go-", label=d2);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel2, fontsize=fsize);
      
      # Legend
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.0, labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   # end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "read_throughput" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Throughput (MB/s) and Total CPU Utilization Percentage for device: " + item["device"] + "</strong></center><BR><BR> \n";
   if (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Throughput (MB/s) and Total CPU Utilization Percentage </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end if


def plot6(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 6: Write Throughput and Total CPU Utilization
   #
   junk1 = "wmb_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Write Throughput and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Write Throughput and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   filename = dirname + "/write_throughput" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.82;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Two_Chart(x_seconds, item["wMB"], x_seconds, time_sum_list, xlabel, ylabel1, 
                ylabel2, d1, d2, fsize, flegsize, filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      box_expansion = 0.88;   # Default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(211);
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["wMB"], marker, label=d11);
         plt.xlabel(" ");
         plt.ylabel(ylabel1, fontsize=fsize);
         ax1.set_xticklabels([]);
      # end for
      plt.grid();
      # Legend
      box = ax1.get_position();
      ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      # Bottom Plot
      ax2 = plt.subplot(212);
      plt.plot(x_seconds, time_sum_list, "go-", label=d2);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel2, fontsize=fsize);
      
      # Legend
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   # end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "write_throughput" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Write Throughput (MB/s) and Total CPU Utilization Percentage for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
       output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Write Throughput (MB/s) and Total CPU Utilization Percentage </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot7(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 7: Read Request complete rate, Write Request complete rate, and Total CPU Utilization
   #
   if (combined_plots == 0):
      output_str = "<H4> \n"
      junk1 = "requests_complete_total_cpu" + str(iloop);
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Requests Complete, Write Requests Complete, and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      junk1 = "requests_complete_total_cpu" + str(iloop);
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Requests Complete, Write Requests Complete, and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
   
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
   d1 = "Read reqs complete";
   d2 = "Write reqs complete";
   d3 = "Total CPU Utilization";
   filename = dirname + "/read_write_requests_complete_rate" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.86;    # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      if (len(d3) > ilongest):
         ilongest = len(d3);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Three_Chart(x_seconds, item["r"], x_seconds, item["w"], x_seconds, time_sum_list, xlabel, ylabel1, 
                  ylabel2, ylabel3, d1, d2, d3, fsize, flegsize, filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      expansion_box = 0.86;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
         if (len(d3) > ilongest):
            ilongest = len(d3);
         # end if
         d33 = item["device"] + " " + d3;
         if (len(d33) > ilongest):
            ilongest = len(d33);
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top plot:
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(311);                 # Define top plot using subplot function
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["r"], marker, label=d11);
         plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
         plt.ylabel(ylabel1, fontsize=fsize);    # Use a 10 pt font for y-axis label
         ax1.set_xticklabels([]);                # get x-axis tick label
         
         plt.xticks(fontsize=fsize);
         plt.yticks(fontsize=fsize);
      # end for
      plt.grid();
      # Legend
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");           # Make legend box have a gray background
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);               # Change the font size of the legend text to 10 pt.
      # end if
      
      # Middle Plot:
      jloop = -1;
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax2 = plt.subplot(312);
         d22 = item["device"] + " " + d2;
         plt.plot(x_seconds, item["w"], marker, label=d22);
         plt.xlabel(" ");
         plt.ylabel(ylabel2, fontsize=fsize);
         ax2.set_xticklabels([]);
         
         plt.xticks(fontsize=fsize);
         plt.yticks(fontsize=fsize);
      # end for
      plt.grid();
      # Legend:
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      # Bottom plot
      ax3 = plt.subplot(313);
      plt.plot(x_seconds, time_sum_list, "go-", label=d3);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel3, fontsize=fsize);
      
      # Legend
      box = ax3.get_position()
      ax3.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg3 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame3 = leg3.get_frame();
      frame3.set_facecolor("0.80");
      for t in leg3.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Either save the plot to a file or display it to the screen
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   # end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "read_write_requests_complete_rate" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Requests Completed Rate (requests/s), Write Requests Completed Rate (requests/s), and Total CPU Utilization Percentage for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Requests Completed Rate (requests/s), Write Requests Completed Rate (requests/s), and Total CPU Utilization Percentage for device </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
# end def



def plot8(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 8: Read Request merge rate, Write Request merge rate, and Total CPU Utilization
   #
   junk1 = "requests_merged_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"   
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Requests Merged rate, Write Requests Merged rate, and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"   
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Read Requests Merged rate, Write Requests Merged rate, and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   d1 = "Read reqs merged";
   d2 = "Write reqs merged";
   d3 = "Total CPU Utilization";
   filename = dirname + "/read_write_requests_merged_rate" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      if (len(d3) > ilongest):
         ilongest = len(d3);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Three_Chart(x_seconds, item["rrqm"], x_seconds, item["wrqm"], x_seconds, time_sum_list,
                  xlabel, ylabel1, ylabel2, ylabel3, d1, d2, d3, fsize, flegsize,
                  filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      expansion_box = 0.87;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
         if (len(d3) > ilongest):
            ilongest = len(d3);
         # end if
         d33 = item["device"] + " " + d3;
         if (len(d33) > ilongest):
            ilongest = len(d33);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top Plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(311);                 # Define top plot using subplot function
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["rrqm"], marker, label=d11);
         plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
         plt.ylabel(ylabel1, fontsize=fsize);    # Use a 10 pt font for y-axis label
         ax1.set_xticklabels([]);                # get x-axis tick label
      # end if
      plt.grid();
      # Legend
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");           # Make legend box have a gray background
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);            # Change the font size of the legend text to 10 pt.
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Middle plot
      jloop = -1;
      
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax2 = plt.subplot(312);
         d22 = item["device"] + " " + d2;
         plt.plot(x_seconds, item["wrqm"], marker, label=d22);
         plt.xlabel(" ");
         plt.ylabel(ylabel2, fontsize=fsize);
         ax2.set_xticklabels([]);
      # end for
      plt.grid();
      # Legend:
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Bottom plot
      ax3 = plt.subplot(313);
      plt.plot(x_seconds, time_sum_list, "go-", label=d3);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel3, fontsize=fsize);
      
      # Legend
      box = ax3.get_position()
      ax3.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg3 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame3 = leg3.get_frame();
      frame3.set_facecolor("0.80");
      for t in leg3.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Either save the plot to a file or display it to the screen
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   # end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "read_write_requests_merged_rate" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Requests Merged Rate (requests/s), Write Requests Merged Rate (requests/s), and Total CPU Utilization Percentage for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Read Requests Merged Rate (requests/s), Write Requests Merged Rate (requests/s), and Total CPU Utilization Percentage </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def


def plot9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 9: Avg. Request Size, Avg. Queue Length, and Total CPU Utilization
   #
   junk1 = "requests_queue_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Request Size, Average Queue Length, and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Request Size, Average Queue Length, and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   d1 = "Avg. Req. Size";
   d2 = "Avg. Queue length";
   d3 = "Total CPU Utilization";
   filename = dirname + "/requests_queue_total_cpu" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      if (len(d3) > ilongest):
         ilongest = len(d3);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Three_Chart(x_seconds, item["avgrqsz"], x_seconds, item["avgqusz"], x_seconds, time_sum_list,
                  xlabel, ylabel1, ylabel2, ylabel3, d1, d2, d3, fsize, flegsize, 
                  filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      box_expansion = 0.87;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
         if (len(d3) > ilongest):
            ilongest = len(d3);
         # end if
         d33 = item["device"] + " " + d3;
         if (len(d33) > ilongest):
            ilongest = len(d33);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(311);                 # Define top plot using subplot function
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["avgrqsz"], marker, label=d11);
         plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
         plt.ylabel(ylabel1, fontsize=fsize);    # Use a 10 pt font for y-axis label
         ax1.set_xticklabels([]);                # get x-axis tick label
      # end if
      plt.grid();
      # Legend
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");           # Make legend box have a gray background
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);            # Change the font size of the legend text to 10 pt.
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Middle plot
      jloop = -1;
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax2 = plt.subplot(312);
         d22 = item["device"] + " " + d2;
         plt.plot(x_seconds, item["avgqusz"], marker, label=d22);
         
         plt.xlabel(" ");
         plt.ylabel(ylabel2, fontsize=fsize);
         ax2.set_xticklabels([]);
      # end for
      plt.grid();
      # Legend:
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Bottom plot
      ax3 = plt.subplot(313);
      plt.plot(x_seconds, time_sum_list, "go-", label=d3);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel3, fontsize=fsize);
      
      # Legend
      box = ax3.get_position()
      ax3.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg3 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame3 = leg3.get_frame();
      frame3.set_facecolor("0.80");
      for t in leg3.get_texts():
         t.set_fontsize(flegsize);
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Either save the plot to a file or display it to the screen
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   # end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "requests_queue_total_cpu" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Request Size (sectors), Average Queue Length, and Total CPU Utilization Percentage for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Request Size (sectors), Average Queue Length, and Total CPU Utilization Percentage </strong></center><BR><BR> \n";
   #end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def


def plot10v10(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
           fsize, item, device_data_list, line_list):
   #
   # Figure 10: Average Wait Times for read, write requests
   # (for V10 format of sysstat)
   #
   junk1 = "avg_wait_time_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   #end if
   
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
   d1 = "Avg. Read Req Time";
   d2 = "Avg. Write Req Time";
   d3 = "Total CPU Utilization";
   filename = dirname + "/avg_request_time_total_cpu" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      if (len(d3) > ilongest):
         ilongest = len(d3);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Three_Chart(x_seconds, item["r_await"], x_seconds, item["w_await"], x_seconds, time_sum_list,
                  xlabel, ylabel1, ylabel2, ylabel3, d1, d2, d3, fsize, flegsize, filename,
                  box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
       # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
         if (len(d3) > ilongest):
            ilongest = len(d3);
         # end if
         d33 = item["device"] + " " + d3;
         if (len(d33) > ilongest):
            ilongest = len(d33);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top Plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(311);                 # Define top plot using subplot function
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["r_await"], marker, label=d11);
         plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
         plt.ylabel(ylabel1, fontsize=fsize);    # Use a 10 pt font for y-axis label
         ax1.set_xticklabels([]);                # get x-axis tick label
      # end if
      plt.grid();
      # Legend
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");           # Make legend box have a gray background
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);            # Change the font size of the legend text to 10 pt.
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Middle plot
      jloop = -1;
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax2 = plt.subplot(312);
         d22 = item["device"] + " " + d2;
         plt.plot(x_seconds, item["w_await"], marker, label=d22);
         plt.xlabel(" ");
         plt.ylabel(ylabel2, fontsize=fsize);
         ax2.set_xticklabels([]);
      # end for
      plt.grid();
      # Legend:
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Bottom plot
      ax3 = plt.subplot(313);
      plt.plot(x_seconds, time_sum_list, "go-", label=d3);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel3, fontsize=fsize);
      
      # Legend
      box = ax3.get_position()
      ax3.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg3 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame3 = leg3.get_frame();
      frame3.set_facecolor("0.80");
      for t in leg3.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Either save the plot to a file or display it to the screen
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   #end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "avg_request_time_total_cpu" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Read Request Time (ms), Average Write Request Time (ms), and Total CPU Utilization </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot10v9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
           fsize, item, device_data_list, line_list):
   #
   # Figure 10: Average Wait Times for requests and total CPU time
   # (for V10 format of sysstat)
   #
   junk1 = "avg_wait_time_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Request Time (ms) and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Average Request Time (ms) and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   #end if
   
   output_str = output_str + " \n";
   output_str = output_str + "<P> \n";
   output_str = output_str + "This figure has two parts. The top graph plots the average \n";
   output_str = output_str + "time (in milliseconds) for requests issued to the device to\n";
   output_str = output_str + "be served. This includes the time spent by the requests in queue \n";
   output_str = output_str + "and the time spent servicing them. The bottom graph plots \n";
   output_str = output_str + "the Total CPU Utilization percentage (User Time + System Time). \n";
   f.write(output_str);
   
   # make the plot
   ylabel1 = "Average Request \n Time (ms)";
   ylabel2 = "Total CPU \n Percentage \n Utilization";
   xlabel = "Time (seconds)";
   d1 = "Avg. Req Time";
   d2 = "Total CPU Utilization";
   filename = dirname + "/avg_request_time_total_cpu" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Two_Chart(x_seconds, item["await"], x_seconds, time_sum_list, xlabel, ylabel1, 
                ylabel2, d1, d2, fsize, flegsize, filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      box_expansion = 0.86;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top Plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(211);                 # Define top plot using subplot function
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["await"], marker, label=d11);
         plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
         plt.ylabel(ylabel1, fontsize=fsize);    # Use a 10 pt font for y-axis label
         ax1.set_xticklabels([]);                # get x-axis tick label
      # end if
      plt.grid();
      # Legend
      box = ax1.get_position()
      ax1.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");           # Make legend box have a gray background
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);            # Change the font size of the legend text to 10 pt.
      # end for
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Bottom plot
      ax2 = plt.subplot(212);
      plt.plot(x_seconds, time_sum_list, "go-", label=d2);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel2, fontsize=fsize);
      
      # Legend
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * expansion_box, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      plt.xticks(fontsize=fsize);
      plt.yticks(fontsize=fsize);
      
      # Either save the plot to a file or display it to the screen
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   #end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "avg_request_time_total_cpu" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Request Time (ms) and Total CPU Utilization for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Average Request Time (ms) and Total CPU Utilization </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end def



def plot11(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list):
   #
   # Figure 11: Percentage CPU Util
   #
   junk1 = "util_cpu_total_cpu" + str(iloop);
   if (combined_plots == 0):
      output_str = "<H4> \n"
      junk1 = "util_cpu_total_cpu" + str(iloop);
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Percentage CPU Time for IO Requests and Total CPU Utilization</a>";
      output_str = output_str + ". Device: " + item["device"] + " \n";
      output_str = output_str + "</H4> \n";
   elif (combined_plots == 1):
      output_str = "<H3> \n"
      junk1 = "util_cpu_total_cpu" + str(iloop);
      output_str = output_str + str(iplot) + ". <a id=\"" + junk1 + "\">Percentage CPU Time for IO Requests and Total CPU Utilization</a>";
      output_str = output_str + "</H3> \n";
   # end if
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
   filename = dirname + "/util_cpu_total_cp" + str(iloop);
   fsize = 8;
   flegsize = 6;
   
   if (combined_plots == 0):
      
      # Compute box_expansion factor:
      box_expansion = 0.82;   # default
      ilongest = 0;
      if (len(d1) > ilongest):
         ilongest = len(d1);
      # end if
      if (len(d2) > ilongest):
         ilongest = len(d2);
      # end if
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      Two_Chart(x_seconds, item["util"], x_seconds, time_sum_list, xlabel, ylabel1, 
                ylabel2, d1, d2, fsize, flegsize, filename, box_expansion);
   elif (combined_plots == 1):
      jloop = -1;
      
      # Compute box_expansion factor:
      box_expansion = 0.90;   # default
      ilongest = 0;
      for item in device_data_list:
         if (len(d1) > ilongest):
            ilongest = len(d1);
         # end if
         d11 = item["device"] + " " + d1;
         if (len(d11) > ilongest):
            ilongest = len(d11);
         # end if
         if (len(d2) > ilongest):
            ilongest = len(d2);
         # end if
         d22 = item["device"] + " " + d2;
         if (len(d22) > ilongest):
            ilongest = len(d22);
         # end if
      # end for
      junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
      expansion_box = round(junk1,2);
      
      # Top plot
      for item in device_data_list:
         jloop = jloop + 1;
         
         marker = line_list[jloop];
         ax1 = plt.subplot(211);
         d11 = item["device"] + " " + d1;
         plt.plot(x_seconds, item["util"], marker, label=d11);
         plt.xlabel(" ");
         plt.ylabel(ylabel1, fontsize=fsize);
         ax1.set_xticklabels([]);
      # end for
      plt.grid();
      # Legend
      box = ax1.get_position();
      ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
      leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame1 = leg1.get_frame();
      frame1.set_facecolor("0.80");
      for t in leg1.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      # Bottom Plot
      ax2 = plt.subplot(212);
      plt.plot(x_seconds, time_sum_list, "go-", label=d2);
      plt.grid();
      plt.xlabel(xlabel);
      plt.ylabel(ylabel2, fontsize=fsize);
      
      # Legend
      box = ax2.get_position()
      ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height])
      leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                        borderpad=0.15, handletextpad=0.2);
      frame2 = leg2.get_frame();
      frame2.set_facecolor("0.80");
      for t in leg2.get_texts():
         t.set_fontsize(flegsize);
      # end for
      
      if (len(filename) == 0):
         plt.show();
      else:
         plt.savefig(filename);
         plt.close();
      # end if
   #end if
   
   # HTML Output:
   output_str = "<center> \n";
   junk1 = "util_cpu_total_cp" + str(iloop) + ".png";
   output_str = output_str + "<img src=\"" + junk1 + "\"> \n";
   if (combined_plots == 0):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time for IO Requests and Total CPU Utilization for device: " + item["device"] + "</strong></center><BR><BR> \n";
   elif (combined_plots == 1):
      output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percentage CPU Time for IO Requests and Total CPU Utilization </strong></center><BR><BR> \n";
   # end if
   output_str = output_str + "<BR><BR> \n";
   output_str = output_str + "</P> \n \n";
   f.write(output_str);
   
# end if







# ===================
# Main Python section
# ===================

if __name__ == '__main__':

   # Get the command line inputs
   input_options = sys.argv;
   combined_plots = 0;
   help_flag = 0;
   for item in input_options:
      if (item == "-c"):
         combined_plots = 1;
      elif (item == "-h"):
         help_flag = 1;
      # end if
   # end for
   input_filename = input_options[-1];
   
   if (help_flag == 1):
      help_out();
      sys.exit();
   # end if
   print "combined_plots = ",combined_plots;
   
   print "iostat plotting script";
   print " ";
   print "input filename: ",input_filename;
   
   # Initialize lists that will store data
   user_list = [];
   nice_list = [];
   system_list = [];
   iowait_list = [];
   steal_list = [];
   idle_list = [];
   date_list = [];
   time_list = [];
   meridian_list = [];
   
   # Initialize variables
   fsize = 8;
   vflag = 0;
   first_flag = 0;
   
   # Master dictionary of device data
   device_data_list = [];
   # Systat V 10 List element is dictionary:
   #   local_dict{"device"} = "device name"
   #   local_dict{"rrqm"} = [];
   #   local_dict{"wrqm"} = [];
   #   local_dict{"r"} = [];
   #   local_dict{"w"} = [];
   #   local_dict{"rMB"} = [];
   #   local_dict{"wMB"} = [];
   #   local_dict{"avgrqsz"} = [];
   #   local_dict{"avgqusz"} = [];
   #   local_dict{"await"} = [];
   #   local_dict{"r_await"} = [];
   #   local_dict{"w_await"} = [];
   #   local_dict{"svctm"} = [];
   #   local_dict{"util"} = [];
   # Systat V 9 List element is dictionary:
   #   local_dict{"device"} = "device name"
   #   local_dict{"rrqm"} = [];
   #   local_dict{"wrqm"} = [];
   #   local_dict{"r"} = [];
   #   local_dict{"w"} = [];
   #   local_dict{"rMB"} = [];
   #   local_dict{"wMB"} = [];
   #   local_dict{"avgrqsz"} = [];
   #   local_dict{"avgqusz"} = [];
   #   local_dict{"await"} = [];
   #   local_dict{"svctm"} = [];
   #   local_dict{"util"} = [];
   
   # flags for controlling flow
   info_flag = 1;       # 0 = don't gather system data, 1 = gather system data
   cpu_flag = -1;       # -1 = don't do anything, 0 = store CPU header info (only done once), 1 = Store CPU info
   device_flag = -1;    # -1 = store Device header info (only done once), 1 = store values, 2 = done
   data_flag = 0;       # -1 = cpu, 1 = device (which set of data is being gathered)
   time_flag = -1;      # -1 = don't read start time information, 1 = read start time information
   
   # loop over lines in input file
   print " ";
   print "reading iostat output file ... ";
   icount = 0;
   for line in open(input_filename,'r').readlines():
      currentline = shlex.split(line);
      
      if (len(currentline) > 0):
         if (device_flag == 0):
            #print "   Read device header";
            device_labels = [];
            device_labels = currentline;
            device_flag = 1;
         elif (device_flag == 1):
            #print "   Read device data";
            local_device = currentline[0];
            #print "      local_device = ",local_device
            if (len(device_data_list) > 0):
               ifind = 0;
               for iloop in range(0, len(device_data_list) ):
                  item = device_data_list[iloop];
                  #for item in device_data_list:
                  if (item["device"] == local_device):
                     #print "         adding data to existing device: ";
                     if (vflag == 9):
                        device_data_list[iloop]["rrqm"].append(float(currentline[1]));
                        device_data_list[iloop]["wrqm"].append(float(currentline[2]));
                        device_data_list[iloop]["r"].append(float(currentline[3]));
                        device_data_list[iloop]["w"].append(float(currentline[4]));
                        device_data_list[iloop]["rMB"].append(float(currentline[5]));
                        device_data_list[iloop]["wMB"].append(float(currentline[6]));
                        device_data_list[iloop]["avgrqsz"].append(float(currentline[7]));
                        device_data_list[iloop]["avgqusz"].append(float(currentline[8]));
                        device_data_list[iloop]["await"].append(float(currentline[9]));
                        device_data_list[iloop]["svctm"].append(float(currentline[10]));
                        device_data_list[iloop]["util"].append(float(currentline[11])); 
                     elif (vflag == 10):
                        device_data_list[iloop]["rrqm"].append(float(currentline[1]));
                        device_data_list[iloop]["wrqm"].append(float(currentline[2]));
                        device_data_list[iloop]["r"].append(float(currentline[3]));
                        device_data_list[iloop]["w"].append(float(currentline[4]));
                        device_data_list[iloop]["rMB"].append(float(currentline[5]));
                        device_data_list[iloop]["wMB"].append(float(currentline[6]));
                        device_data_list[iloop]["avgrqsz"].append(float(currentline[7]));
                        device_data_list[iloop]["avgqusz"].append(float(currentline[8]));
                        device_data_list[iloop]["await"].append(float(currentline[9]));
                        device_data_list[iloop]["r_await"].append(float(currentline[10]));
                        device_data_list[iloop]["w_await"].append(float(currentline[11]));
                        device_data_list[iloop]["svctm"].append(float(currentline[12]));
                        device_data_list[iloop]["util"].append(float(currentline[13]));
                     #end if           
                     ifind = 1;
                  # end if
               # end for
               if (ifind == 0):
                  #print "         creating new device ifind == 0";
                  if (first_flag == 0):
                     if (len(currentline) == 12):
                        vflag = 9;
                        print "Using Version 9 format of sysstat tools";
                     elif (len(currentline) == 14):
                        vflag = 10;
                        print "Using Version 10 format of sysstat tools";
                     else:
                        print "Error: each line has ",len(currentline)," elements"
                        print "This code is designed for 12 elemenets for sysstat V9";
                        print "or 14 elements for sysstat V10";
                        print "Stopping";
                        sys.exit();
                     # end if
                     first_flag = 1;
                  # end if
                  local_dict = {};
                  if (vflag == 9):
                     local_dict["device"] = local_device;
                     local_dict["rrqm"]=[float(currentline[1])];
                     local_dict["wrqm"]=[float(currentline[2])];
                     local_dict["r"]=[float(currentline[3])]; 
                     local_dict["w"]=[float(currentline[4])];
                     local_dict["rMB"]=[float(currentline[5])];
                     local_dict["wMB"]=[float(currentline[6])];
                     local_dict["avgrqsz"]=[float(currentline[7])];
                     local_dict["avgqusz"]=[float(currentline[8])];
                     local_dict["await"]=[float(currentline[9])];
                     local_dict["svctm"]=[float(currentline[10])];
                     local_dict["util"]=[float(currentline[11])];
                     #print "      local_dict = ",local_dict
                     device_data_list.append(local_dict);
                  elif (vflag == 10):
                     local_dict["device"] = local_device;
                     local_dict["rrqm"]=[float(currentline[1])];
                     local_dict["wrqm"]=[float(currentline[2])];
                     local_dict["r"]=[float(currentline[3])]; 
                     local_dict["w"]=[float(currentline[4])];
                     local_dict["rMB"]=[float(currentline[5])];
                     local_dict["wMB"]=[float(currentline[6])];
                     local_dict["avgrqsz"]=[float(currentline[7])];
                     local_dict["avgqusz"]=[float(currentline[8])];
                     local_dict["await"]=[float(currentline[9])];
                     local_dict["r_await"]=[float(currentline[10])];
                     local_dict["w_await"]=[float(currentline[11])];
                     local_dict["svctm"]=[float(currentline[12])];
                     local_dict["util"]=[float(currentline[13])];
                     #print "      local_dict = ",local_dict
                     device_data_list.append(local_dict);
                  # end if
               # end if
            else:
               #print "         creating new device else";
               if (first_flag == 0):
                  if (len(currentline) == 12):
                     vflag = 9;
                     print "Using Version 9 format of sysstat tools";
                  elif (len(currentline) == 14):
                     vflag = 10;
                     print "Using Version 10 format of sysstat tools";
                  else:
                     print "Error: each line has ",len(currentline)," elements"
                     print "This code is designed for 12 elemenets for sysstat V9";
                     print "or 14 elements for sysstat V10";
                     print "Stopping";
                     sys.exit();
                  # end if
                  first_flag = 1;
               # end if
               local_dict = {};
               if (vflag == 9):
                  local_dict["device"] = local_device;
                  local_dict["rrqm"]=[float(currentline[1])];
                  local_dict["wrqm"]=[float(currentline[2])];
                  local_dict["r"]=[float(currentline[3])]; 
                  local_dict["w"]=[float(currentline[4])];
                  local_dict["rMB"]=[float(currentline[5])];
                  local_dict["wMB"]=[float(currentline[6])];
                  local_dict["avgrqsz"]=[float(currentline[7])];
                  local_dict["avgqusz"]=[float(currentline[8])];
                  local_dict["await"]=[float(currentline[9])];
                  local_dict["svctm"]=[float(currentline[10])];
                  local_dict["util"]=[float(currentline[11])];
                  device_data_list.append(local_dict);
               elif (vflag == 10):
                  local_dict["device"] = local_device;
                  local_dict["rrqm"]=[float(currentline[1])];
                  local_dict["wrqm"]=[float(currentline[2])];
                  local_dict["r"]=[float(currentline[3])]; 
                  local_dict["w"]=[float(currentline[4])];
                  local_dict["rMB"]=[float(currentline[5])];
                  local_dict["wMB"]=[float(currentline[6])];
                  local_dict["avgrqsz"]=[float(currentline[7])];
                  local_dict["avgqusz"]=[float(currentline[8])];
                  local_dict["await"]=[float(currentline[9])];
                  local_dict["r_await"]=[float(currentline[10])];
                  local_dict["w_await"]=[float(currentline[11])];
                  local_dict["svctm"]=[float(currentline[12])];
                  local_dict["util"]=[float(currentline[13])];
                  device_data_list.append(local_dict);
               # end if
               #print "      local_dict = ",local_dict
            # end if
               
         elif (cpu_flag == 1):
            #print "   Reading and Storing CPU values";
            user_list.append(float(currentline[0]));
            nice_list.append(float(currentline[1]));
            system_list.append(float(currentline[2]));
            iowait_list.append(float(currentline[3]));
            steal_list.append(float(currentline[4]));
            idle_list.append(float(currentline[5]));
            #print "      user_list = ",user_list
            #print "      nice_list = ",nice_list
            #print "      system_list = ",system_list
            #print "      iowait_list = ",iowait_list
            #print "      steal_list = ",steal_list
            #print "      idle_list = ",idle_list
            cpu_flag = -1;
            device_flag = 0;
         elif (cpu_flag == 0):
            #print "      Reading and storing CPU headers";
            cpu_labels = [];
            cpu_labels = currentline;
	    cpu_flag = 1;
            #print "      cpu_labels = ",cpu_labels
         elif (time_flag == 1):
            #print "   Read time information";
            date_list.append(currentline[0].replace("/"," "));
            # if meridian is PM then need to add 12 hours to time_list
            if (currentline[2] == "PM"):
               junk1 = currentline[1].replace(":"," ");
               junk2 = shlex.split(junk1);
               if ( int(junk2[0]) < 12):
                  junk3 = int(junk2[0]) + 12;
               elif (int(junk2[0]) == 12):
                  junk3 = int(junk2[0]);
               # end if
               junk4 = str(junk3) + ":" + junk2[1] + ":" + junk2[2];
               time_list.append(junk4);
            else:
               time_list.append(currentline[1]);
            # end if
            #print "      date_list = ",date_list
            #print "      time_list = ",time_list
            meridian_list.append(currentline[2]);
            time_flag = -1;
            cpu_flag = 0;
            icount = icount + 1;
         elif (info_flag == 1):
            #print "   Read system information";
            system_info = {};
            system_info["OS"] = currentline[0];
            system_info["kernel"] = currentline[1];
            system_info["system_name"] = currentline[2][1:len(currentline[2])-1];
            system_info["date"] = currentline[3];
            system_info["CPU"] = currentline[4];
            system_info["cores"] = currentline[5][1:];
            info_flag = 0;
            time_flag = 1;
            #print "   system_info:",system_info
         # end if
      else:
         #print "Finished reading section - get ready for next section";
         if (device_flag == 1):
            device_flag = -1;
            time_flag = 1;
            cpu_flag = -1;
            info_flag = 0;
         # end if
      # end if
   # end for
   print "Finished reading ",icount," data points for ",len(device_data_list)," devices.";
   print "Creating plots and HTML report";
   
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
   output_str = output_str + input_filename + ". The devices analyzed are: \n";
   output_str = output_str + "<UL> \n";
   for item in device_data_list:
      output_str = output_str + "   <LI>" + item["device"] + " \n";
   # end if
   if (combined_plots == 0):
      output_str = output_str + "</UL> \n";
      output_str = output_str + "For each devices there are a series of plots of the output \n";
      output_str = output_str + "from iostat that was captured. The report is contained in a\n";
      output_str = output_str + "subdirectory HTML_REPORT. In that directory you will find a \n";
      output_str = output_str + "file name report.html. Just open that file in a browser \n";
      output_str = output_str + "and you will see the plots. Please note that all plots are \n";
      output_str = output_str + "referenced to the beginning time of the iostat run. \n";
      output_str = output_str + "</P>\n";
      output_str = output_str + " \n";
      f.write(output_str);
   elif(combined_plots == 1):
      output_str = output_str + "</UL> \n";
      output_str = output_str + "There are a series of plots from the captured iostat output \n";
      output_str = output_str + "where all devices are plotted together where possible. \n";
      output_str = output_str + "The report is contained in a\n";
      output_str = output_str + "subdirectory HTML_REPORT. In that directory you will find a \n";
      output_str = output_str + "file name report.html. Just open that file in a browser \n";
      output_str = output_str + "and you will see the plots. Please note that all plots are \n";
      output_str = output_str + "referenced to the beginning time of the iostat run. \n";
      output_str = output_str + "</P>\n";
      output_str = output_str + " \n";
      f.write(output_str);
   # end if
   
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
   if (combined_plots == 0):
      output_str = "<P> \n";
      output_str = output_str + "Below are hyperlinks to various plots within the report \n";
      output_str = output_str + "for each device. \n";
      output_str = output_str + "<BR><BR> \n";
      f.write(output_str);
   elif (combined_plots == 1):
      output_str = "<P> \n";
      output_str = output_str + "Below are hyperlinks to various plots within the report \n";
      output_str = output_str + "where all of the devices are plotted together on each chart. \n";
      output_str = output_str + "<BR><BR> \n";
      f.write(output_str);
   # end if
   iloop = -1;
   plots_per_device = 11;
   if (combined_plots == 0):
      max_plots = plots_per_device * len(device_data_list);
   elif (combined_plots == 1):
      max_plots = plots_per_device;
   #end if
   if (combined_plots == 0):
      for item in device_data_list:
         iloop = iloop + 1;
         output_str = "<strong>" + item["device"] + "</strong>: \n";
         junk1 = (iloop)*plots_per_device+1;
         output_str = output_str + "<OL start=" + str(junk1) + "> \n";
         junk1 = "cpu_utilization" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">CPU Utilization</a> \n";
         junk1 = "iowait_cpu_utilization" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">IOwait Percentage Time</a> \n";
         junk1 = "steal_cpu_utilization" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Steal Percentage Time</a> \n";
         junk1 = "idle_cpu_utilization" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Idle Percentage Time</a> \n";
         junk1 = "rmb_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Throughput and Total CPU Utilization</a> \n";
         junk1 = "wmb_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Write Throughput and Total CPU Utilization</a> \n";
         junk1 = "requests_complete_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Requests Complete Rate, Write Requests Complete Rate, and Total CPU Utilization</a> \n";
         junk1 = "requests_merged_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Requests Merged Rate, Write Requests Merged Rate, and Total CPU Utilization</a> \n";
         junk1 = "requests_queue_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Request Size, Average Queue Length, and Total CPU Utilization Percentage</a> \n";
         junk1 = "avg_wait_time_total_cpu" + str(iloop);
         if (vflag == 10):
            output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Read Request Time, Average Write Request Time, and Total CPU Utilization</a> \n";
         elif (vflag == 9):
            output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Request Time and Total CPU Utilization</a> \n";
         # end if
         junk1 = "util_cpu_total_cpu" + str(iloop);
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Percentage CPU Time for IO Requests and Total CPU Utilization</a> \n";
         output_str = output_str + "</OL> \n";
         output_str = output_str + "</P> \n";
         output_str = output_str + " \n";
         f.write(output_str);
      # end if
   elif (combined_plots == 1):
      iloop = 0;
      iloop = iloop + 1;
      output_str = "<OL start=" + str(iloop) + "> \n";
      junk1 = "cpu_utilization" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">CPU Utilization</a> \n";
      junk1 = "iowait_cpu_utilization" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">IOwait Percentage Time</a> \n";
      junk1 = "steal_cpu_utilization" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Steal Percentage Time</a> \n";
      junk1 = "idle_cpu_utilization" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Idle Percentage Time</a> \n";
      junk1 = "rmb_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Throughput and Total CPU Utilization</a> \n";
      junk1 = "wmb_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Write Throughput and Total CPU Utilization</a> \n";
      junk1 = "requests_complete_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Requests Complete Rate, Write Requests Complete Rate, and Total CPU Utilization</a> \n";
      junk1 = "requests_merged_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Read Requests Merged Rate, Write Requests Merged Rate, and Total CPU Utilization</a> \n";
      junk1 = "requests_queue_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Request Size, Average Queue Length, and Total CPU Utilization Percentage</a> \n";
      junk1 = "avg_wait_time_total_cpu" + str(iloop);
      if (vflag == 10):
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Read Request Time, Average Write Request Time, and Total CPU Utilization</a> \n";
      elif (vflag == 9):
         output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Average Request Time and Total CPU Utilization</a> \n";
      # end if
      junk1 = "util_cpu_total_cpu" + str(iloop);
      output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Percentage CPU Time for IO Requests and Total CPU Utilization</a> \n";
      output_str = output_str + "</OL> \n";
      output_str = output_str + "</P> \n";
      output_str = output_str + " \n";
      f.write(output_str);
   #endif
   
   # Create array of line colors/styles:
   # http://matplotlib.org/api/artist_api.html#matplotlib.lines.Line2D.lineStyles
   # line_style = ['-', '--', '-.'];
   # line_marker  = ['o', '^', 's', '*', '+', '<', '>', 'v'];
   color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k'];
   line_style = ['o-', '^--', 's-.', '*-', '<--', '>-.', 'v-', 'o--'];
   line_list = [];
   for line_type in line_style:
      for color in color_list:
         junk2 = color + line_type;
         line_list.append(junk2);
      # end for
   # end for
   
   #
   # Actually create the plots!!
   #
   if (combined_plots == 0):
      # Loop over each device and create plots and HTML:
      iloop = -1;
      iplot = 0;
      for item in device_data_list:
         iloop = iloop + 1;
         
         print "Device: ",item["device"];
         output_str = "<HR> \n";
         f.write(output_str);
         
         output_str = "<H3>Device: " + item["device"] + "</H3> \n";
         f.write(output_str);
         
         # Figure 1: Various CPU percentages (user, system, nice) vs. time (3 subplots)
         iplot = iplot + 1;
         plot1(iloop, iplot, combined_plots, f, dirname, x_seconds, user_list, system_list, 
               nice_list, fsize, item);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 2: iowait percentage time
         iplot = iplot + 1;
         fsize = 6;
         plot2(iloop, iplot, combined_plots, f, dirname, x_seconds, iowait_list, 
               fsize, item);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 3: Steal Time
         iplot = iplot + 1;
         plot3(iloop, iplot, combined_plots, f, dirname, x_seconds, steal_list, 
               fsize, item);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 4: Idle Time
         iplot = iplot + 1;
         plot4(iloop, iplot, combined_plots, f, dirname, x_seconds, idle_list,
               fsize, item);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 5: Read Throughput and Total CPU Utilization
         iplot = iplot + 1;
         fsize = 6;
         plot5(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
               fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 6: Write Throughput and Total CPU Utilization
         iplot = iplot + 1;
         plot6(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
               fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 7: Read Request complete rate, Write Request complete rate, and Total CPU Utilization
         # HTML report output (opt of section)
         iplot = iplot + 1;
         fsize = 6
         plot7(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
               fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
         
         # Figure 8: Read Request merge rate, Write Request merge rate, and Total CPU Utilization
         iplot = iplot + 1;
         plot8(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
               fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
      
         # Figure 9: Avg. Request Size, Avg. Queue Length, and Total CPU Utilization
         iplot = iplot + 1;
         plot9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
               fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
      
         # Figure 10: Average Wait Times for read, write requests
         iplot = iplot + 1;
         if (vflag == 9):
            plot10v9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
                     fsize, item, device_data_list, line_list);
         elif (vflag == 10):
            plot10v10(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
                      fsize, item, device_data_list, line_list);
         # end if
         print "   Finished Plot ",iplot," of ",max_plots;
      
         # Figure 11: Percentage CPU Util
         iplot = iplot + 1;
         plot11(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
                fsize, item, device_data_list, line_list);
         print "   Finished Plot ",iplot," of ",max_plots;
      # end for
      
   elif (combined_plots == 1):
      # For each plot, Loop over each device and create plot and HTML:
      iloop = 1;
      iplot = 0;
       
      output_str = "<HR> \n";
      f.write(output_str);
      
      # Figure 1: Various CPU percentages (user, system, nice) vs. time (3 subplots)
      iplot = iplot + 1;
      plot1(iloop, iplot, combined_plots, f, dirname, x_seconds, user_list, system_list, 
            nice_list, fsize, item);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 2: iowait percentage time
      iplot = iplot + 1;
      plot2(iloop, iplot, combined_plots, f, dirname, x_seconds, iowait_list, 
            fsize, item);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 3: Steal Time
      iplot = iplot + 1;
      plot3(iloop, iplot, combined_plots, f, dirname, x_seconds, steal_list, 
            fsize, item);
      print "   Finished Plot ",iplot," of ",max_plots;
         
      # Figure 4: Idle Time
      iplot = iplot + 1;
      plot4(iloop, iplot, combined_plots, f, dirname, x_seconds, idle_list,
            fsize, item);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 5: Read Throughput and Total CPU Utilization
      iplot = iplot + 1;
      fsize = 6;
      plot5(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
           fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 6: Write Throughput and Total CPU Utilization
      iplot = iplot + 1;
      plot6(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
            fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 7: Read Request complete rate, Write Request complete rate, and Total CPU Utilization
      iplot = iplot + 1;
      plot7(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
          fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;
      
      # Figure 8: Read Request merge rate, Write Request merge rate, and Total CPU Utilization
      iplot = iplot + 1;
      plot8(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
            fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;

      # Figure 9: Avg. Request Size, Avg. Queue Length, and Total CPU Utilization
      iplot = iplot + 1;
      plot9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
            fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;

      # Figure 10: Average Wait Times for read, write requests
      iplot = iplot + 1;
      if (vflag == 9):
         plot10v9(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
                  fsize, item, device_data_list, line_list);
      elif (vflag == 10):
         plot10v10(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
                  fsize, item, device_data_list, line_list);
      # end if
      print "   Finished Plot ",iplot," of ",max_plots;

      # Figure 11: Percentage CPU Util
      iplot = iplot + 1;
      plot11(iloop, iplot, combined_plots, f, dirname, x_seconds, time_sum_list,
             fsize, item, device_data_list, line_list);
      print "   Finished Plot ",iplot," of ",max_plots;
   # end of
   print "Finished. Please open the document HTML/report.html in a browser.";
   
   # Start of Pickling
   # =================
   if (pickle_success > 0):
      # Open file for pickling
      pickle_file = open('iostat_file.pickle', 'w')
      
      # Big dictionary:
      iostat_dict = {};
      
      # Create CPU dictionary for pickling:
      cpu_data = {};
      cpu_data["user_list"] = user_list;
      cpu_data["nice_list"] = nice_list;
      cpu_data["system_list"] = system_list;
      cpu_data["iowait_list"] = iowait_list;
      cpu_data["steal_list"] = steal_list;
      cpu_data["idle_list"] = idle_list;
      cpu_data["cpu_labels"] = cpu_labels;
      cpu_data["time_sum_list"] = time_sum_list;
      cpu_data["version"] = vflag;
      
      # Time dictionary for pickling:
      time_data = {};
      time_data["date_list"] = date_list;
      time_data["time_list"] = time_list;
      time_data["meridian_list"] = meridian_list;
      
      # Device data
      #device_data = {};
      #device_data["rrqm"] = device_data_list["rrqm"];
      #device_data["wrqm"] = device_data_list["wrqm"];
      #device_data["r"] = device_data_list["r"];
      #device_data["w"] = device_data_list["w"];
      #device_data["rMB"] = device_data_list["rMB"];
      #device_data["wMB"] = device_data_list["wMB"];
      #device_data["avgrqsz"] = device_data_list["avgrqsz"];
      #device_data["avgqusz"] = device_data_list["avgqusz"];
      #device_data["await"] = device_data_list["await"];
      #device_data["r_await"] = device_data_list["r_await"];
      #device_data["w_await"] = device_data_list["w_await"];
      #device_data["svctm"] = device_data_list["svctm"];
      #device_data["util"] = device_data_list["util"];
      
      # Assemble the big pickle;
      iostat_dict["device_data_list"] = device_data_list;
      iostat_dict["cpu_data"] = cpu_data;
      iostat_dict["system_info"] = system_info;
      iostat_dict["time_data"] = time_data;
      iostat_dict["x_seconds"] = x_seconds;
      
      # Write list to pickle file
      pickle.dump(iostat_dict, pickle_file);
      
      # Close pickle file
      pickle_file.close();
   # end if
# end
