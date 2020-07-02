using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace try_python_connection
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {


        public Data data { get; set; }
        public TestViewerWindow testViewerWindow { get; set; }

        public Process process;
        public delegate void DataFunc(string data);
        public MainWindow()
        {

            data = new Data();

            InitializeComponent();
            ((INotifyCollectionChanged)playlistListView.Items).CollectionChanged += playlistListViewCollectionChanged;
            
            data.fPlaylist = new ObservableCollection<PlaylistItem>();
            DataContext = data;
            ctestListView.ItemsSource = data.cTests;
            //ftestListView.ItemsSource = data.fTests.se(x=> x.test["name"].Split(':')[0] == featuresListView.SelectedItem.ToString());
            playlistListView.ItemsSource = data.fPlaylist;

            refreshDevices();
            //Task task = new Task(()=> { run_cmd("adb.exe", "devices", (s,e)=> { if (e.Data != null && Regex.IsMatch(e.Data, @"device\b")) { data.devices.Add(e.Data.Split(null)[0]); } Debug.WriteLine(data.devices.Count.ToString()); },(s,e)=> { } ,(s,e)=> { if (data.devices.Count == 0) { data.devices = null; }   } ); });
            //task.Start();

            //mainListView.SelectedIndex = 0;
        }

        private void playlistListViewCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            if(playlistListView.SelectedIndex != -1)
                rtbOutput.SetRtf(((PlaylistItem)playlistListView.SelectedItem).output);
            CheckEnableBtnRun();
        }


        ////////////////////private void run_cmd(string cmd, string args, DataFunc OutputDataFunc, DataFunc ErrorDataFunc, EventHandler ExitEventHandler = null)
        ////////////////////{


        ////////////////////    ProcessStartInfo StartInfo = new ProcessStartInfo()
        ////////////////////    {
        ////////////////////        FileName = cmd,
        ////////////////////        Arguments = args,
        ////////////////////        CreateNoWindow = true,
        ////////////////////        UseShellExecute = false,
        ////////////////////        ErrorDialog = false,
        ////////////////////        RedirectStandardInput = false,
        ////////////////////        RedirectStandardOutput = true,
        ////////////////////        RedirectStandardError = true,

        ////////////////////        Verb = "runas",
        ////////////////////    };




        ////////////////////    using (var process = Process.Start(StartInfo))
        ////////////////////    {
        ////////////////////        process.OutputDataReceived += (sender, eventArgs) => App.Current.Dispatcher.Invoke(() => OutputDataFunc(eventArgs.Data));
        ////////////////////        process.ErrorDataReceived += (sender, eventArgs) => App.Current.Dispatcher.Invoke(() => ErrorDataFunc(eventArgs.Data));

        ////////////////////        process.BeginOutputReadLine();
        ////////////////////        process.BeginErrorReadLine();

        ////////////////////        process.WaitForExit();
        ////////////////////    }

        ////////////////////    //process.OutputDataReceived += OutputDataReceivedEventHandler;
        ////////////////////    ////process.OutputDataReceived += (s, e) => { data.output += e.Data; };
        ////////////////////    //process.ErrorDataReceived += ErorrDataReceivedEventHandler;
        ////////////////////    //process.Exited += ExitEventHandler;





        ////////////////////    //process.Start();
        ////////////////////    //process.BeginOutputReadLine();
        ////////////////////    //process.BeginErrorReadLine();
        ////////////////////    //process.WaitForExit();

        ////////////////////    //process.Close();
        ////////////////////    //process.Kill();




        ////////////////////    //ProcessStartInfo start = new ProcessStartInfo();
        ////////////////////    //start.FileName = cmd;
        ////////////////////    //start.Arguments = string.Format(args);
        ////////////////////    //start.UseShellExecute = false;
        ////////////////////    //start.RedirectStandardOutput = true;
        ////////////////////    //start.RedirectStandardError = true;
        ////////////////////    //start.CreateNoWindow = true;
        ////////////////////    //using (Process process = Process.Start(start))
        ////////////////////    //{

        ////////////////////    //    //process.OutputDataReceived += (s, e) => data.output += ("\n" + e.Data);
        ////////////////////    //    //process.ErrorDataReceived += (s, e) => data.output += ("\n" + e.Data);
        ////////////////////    //    //process.BeginOutputReadLine();
        ////////////////////    //    //process.BeginErrorReadLine();
        ////////////////////    //    //process.WaitForExit(2000);

        ////////////////////    //    using (StreamReader reader = process.StandardOutput)
        ////////////////////    //    {
        ////////////////////    //        string standard_output;
        ////////////////////    //        //while ((standard_output = reader.ReadLine()) != null)
        ////////////////////    //        //{
        ////////////////////    //        //    txtOutput.Text += standard_output;
        ////////////////////    //        //}

        ////////////////////    //        string result = reader.ReadToEnd();
        ////////////////////    //        data.output += result;

        ////////////////////    //    }


        ////////////////////    //}



        ////////////////////}


        private async Task<int> run_cmd(string cmd, string args, DataReceivedEventHandler OutputDataReceivedEventHandler, DataReceivedEventHandler ErorrDataReceivedEventHandler, EventHandler ExitEventHandler = null)
        {
            int i;

            //process = new Process()
            //{
            var StartInfo = new ProcessStartInfo()
            {
                FileName = cmd,
                Arguments = args,
                CreateNoWindow = true,
                UseShellExecute = false,
                ErrorDialog = false,
                RedirectStandardInput = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                Verb = "runas",
            };
            //    EnableRaisingEvents = true,


            //};

            string ss = @"{\rtf1\ansi\deff0
                          {\colortbl;\red0\green0\blue0;\red255\green0\blue0; }
                          This line is the default color\line
                          \cf2
                          This line is red\line
                          \cf1
                          This line \i  is the \i0 default color
                          }";

    

            using (var process = Process.Start(StartInfo))
            {
                process.OutputDataReceived += OutputDataReceivedEventHandler;
                //process.OutputDataReceived += (s, e) => { data.output += e.Data; };
                process.ErrorDataReceived += ErorrDataReceivedEventHandler;
                process.Exited += ExitEventHandler;

               // process.OutputDataReceived += (sender, eventArgs) => App.Current.Dispatcher.Invoke(() => rtbOutput.SetRtf(eventArgs.Data));
                //process.ErrorDataReceived += (sender, eventArgs) => App.Current.Dispatcher.Invoke(() => rtbOutput.AppendText("\n" + eventArgs.Data, "Red"));

                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                await process.WaitForExitAsync();
                i = process.ExitCode;

                if (!process.HasExited) process.Kill();
            }
            //process.OutputDataReceived += OutputDataReceivedEventHandler;
            ////process.OutputDataReceived += (s, e) => { data.output += e.Data; };
            //process.ErrorDataReceived += ErorrDataReceivedEventHandler;
            //process.Exited += ExitEventHandler;




            //process.Start();
            //process.BeginOutputReadLine();
            ////process.BeginErrorReadLine();
            //await process.WaitForExitAsync();
            //process.Close();
            //var i = process.ExitCode;

            //if (!process.HasExited) process.Kill();



            //ProcessStartInfo start = new ProcessStartInfo();
            //start.FileName = cmd;
            //start.Arguments = string.Format(args);
            //start.UseShellExecute = false;
            //start.RedirectStandardOutput = true;
            //start.RedirectStandardError = true;
            //start.CreateNoWindow = true;
            //using (Process process = Process.Start(start))
            //{

            //    //process.OutputDataReceived += (s, e) => data.output += ("\n" + e.Data);
            //    //process.ErrorDataReceived += (s, e) => data.output += ("\n" + e.Data);
            //    //process.BeginOutputReadLine();
            //    //process.BeginErrorReadLine();
            //    //process.WaitForExit(2000);

            //    using (StreamReader reader = process.StandardOutput)
            //    {
            //        string standard_output;
            //        //while ((standard_output = reader.ReadLine()) != null)
            //        //{
            //        //    txtOutput.Text += standard_output;
            //        //}

            //        string result = reader.ReadToEnd();
            //        data.output += result;

            //    }


            //}
            //await Task.Delay(5000);

            return i;

        }


        private void ListViewItem_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            testViewerWindow = new TestViewerWindow();
            testViewerWindow.testViewerWindowViewModel.testViewerItems = data.fTestViewerItems;
            testViewerWindow.ShowInTaskbar = false;
            testViewerWindow.Owner = this;
            testViewerWindow.ShowDialog();
        }

        private void Button_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {

        }

        private void FtestListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ftestListView.SelectedItem != null && ((FTest)ftestListView.SelectedItem).supportedApps.Count == 0)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem);
        }

        private void AppsListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ftestListView.SelectedItem != null)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem);



        }




        private void FeaturesListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            data.featureTests.Filter = (item) => { return (item as FTest).details["name"].ToString().Split(':')[0] == (string)featuresListView.SelectedItem ? true : false; };

        }

        private async void BtnRun_Click(object sender, RoutedEventArgs e)
        {
            //////////////////////string path1 = @"C:\Users\israel\PycharmProjects\imageProccessing\final_project\dist\main.exe";
            //////////////////////Task task = new Task(() =>
            //////////////////////{
            //////////////////////    run_cmd(path1, string.Format("{0} {1} {2} {3} {4}", "f", "\"Send an offensive message through whatsapp\"", "WhatsApp", "emulator-5554", "0915f9dd355b3105"),
            //////////////////////      (s) => { rtbOutput.AppendText("\n" + s, "Black"); },
            //////////////////////      (s) =>
            //////////////////////      {
            //////////////////////          rtbOutput.AppendText("\n" + s, "Red");
            //////////////////////      });
            //////////////////////});
            //////////////////////task.Start();


            run_test();


            //string path1 = @"C:\Users\Chani\PycharmProjects\final project\dist\main.exe";
            //Task task = new Task(() => { run_cmd(path1, string.Format("{0} {1} {2} {3} {4}","f", "\"Recive an offensive message\"", "WhatsApp", "emulator-5554", "0915f9dd355b3105"), (s, ev) => { data.output += ("\n" + ev.Data);  Debug.WriteLine("--------------------"); }, (s, ev) => { data.output += ("\n" + ev.Data); }); });
            //task.Start();


        }

        private async void run_test()
        {
            foreach (var test in data.fPlaylist)
                test.status = Status.waiting;


            foreach(var fp in data.fPlaylist)
            {
                playlistListView.SelectedItem = fp;

                fp.status = Status.runing;
                string path = @"C:\Users\chani\PycharmProjects\final project\dist\main.exe";

                int exitCode = await run_cmd
                (
                    path,
                    string.Format("{0} {1} {2} {3} {4}","f", "\"" + fp.name + "\"", fp.appName, fDeviceComboBox.SelectedItem, cDeviceComboBox.SelectedItem),
                    (s, ev) =>
                    {
                    
                    
                        fp.output += (ev.Data);
                        App.Current.Dispatcher.Invoke(() => rtbOutput.SetRtf(fp.output));
                    
                            
                    },
                    (s, ev) =>
                    {
                       
                        fp.output += ("\\cf2"+ ev.Data+ "\\line");
                        App.Current.Dispatcher.Invoke(() => rtbOutput.SetRtf(fp.output));
                    },
                    (s, ev) =>
                    {

                    }



                );

                //Debug.WriteLine(exitCode);
                switch (exitCode)
                {
                    case 0:
                        fp.status = Status.PASSED;
                        break;

                    case 1:
                        fp.status = Status.FAILED;
                        break;

                    case -1:
                        fp.status = Status.ERROR;
                        break;


                }







            }


        }

        private void BtnRemoveTest_Click(object sender, RoutedEventArgs e)
        {

            data.fTests.RemoveAt(data.fTests.IndexOf((FTest)ftestListView.SelectedItem) + 1);
            //data.saveFtestToXML(data.fTests.ToList());
        }

        private void btnRefreshDevices_Click(object sender, RoutedEventArgs e)
        {
            //////////////////////Task task = new Task(() => { run_cmd("adb.exe", "devices", (s) => { if (s != null && Regex.IsMatch(s, @"device\b")) { data.devices.Add(s.Split(null)[0]); } Debug.WriteLine(data.devices.Count.ToString()); }, (s) => { }, (s, ev) => { if (data.devices.Count == 0) { data.devices = null; } }); });
            //////////////////////task.Start();
           refreshDevices();
        }

        private async void refreshDevices()
        {

            data.devices = null;
            await run_cmd
                (
                    "adb.exe",
                    "devices",
                    (s, ev) =>
                        {
                            if (ev.Data != null && Regex.IsMatch(ev.Data, @"device\b"))
                            {
                                App.Current.Dispatcher.BeginInvoke(new Action(() =>
                                {
                                    if (data.devices == null) data.devices = new ObservableCollection<string>();
                                    data.devices.Add(ev.Data.Split(null)[0]);
                                }));
                            }

                        },
                    (s, ev) => { },
                    (s, ev) => { }
                );

        }

        private void DeviceComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ComboBox otherComboBox;
            if (((ComboBox)sender) == fDeviceComboBox)
                otherComboBox = cDeviceComboBox;
            else
                otherComboBox = fDeviceComboBox;


            if (((ComboBox)sender).SelectedItem == otherComboBox.SelectedItem)
                otherComboBox.SelectedIndex = -1;

            if (data.devices != null && data.devices.Count == 2)
                switch (((ComboBox)sender).SelectedIndex)
                {
                    case 0:
                        otherComboBox.SelectedIndex = 1;
                        break;
                    case 1:
                        otherComboBox.SelectedIndex = 0;
                        break;
                }


            CheckEnableBtnRun();


        }

        private void CheckEnableBtnRun()
        {
            if (fDeviceComboBox.SelectedIndex != -1 && cDeviceComboBox.SelectedIndex != -1 && data.fPlaylist.Count > 0)
                btnRun.IsEnabled = true;
            else
                btnRun.IsEnabled = false;
        }

        private void PlaylistListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
           // CheckEnableBtnRun();
        }


        private void RunDispatcher(Action action)
        {
            App.Current.Dispatcher.BeginInvoke(action);
        }

        private void rtbOutput_TextChanged(object sender, TextChangedEventArgs e)
        {
           // ((Xceed.Wpf.Toolkit.RichTextBox)e.Source).SetRtf(((Xceed.Wpf.Toolkit.RichTextBox)e.Source).Text);
        }
    }


    public static class exProcessExtensions
    {
        /// <summary>
        /// Waits asynchronously for the process to exit.
        /// </summary>
        /// <param name="process">The process to wait for cancellation.</param>
        /// <param name="cancellationToken">A cancellation token. If invoked, the task will return 
        /// immediately as canceled.</param>
        /// <returns>A Task representing waiting for the process to end.</returns>
        public static Task WaitForExitAsync(this Process process,
            CancellationToken cancellationToken = default(CancellationToken))
        {
            if (process.HasExited) return Task.CompletedTask;

            var tcs = new TaskCompletionSource<object>();
            process.EnableRaisingEvents = true;
            process.Exited += (sender, args) => tcs.TrySetResult(null);
            if (cancellationToken != default(CancellationToken))
                cancellationToken.Register(() => tcs.SetCanceled());

            return process.HasExited ? Task.CompletedTask : tcs.Task;
        }
    }


    public static class RichTextBoxExtensions
    {
        public static void AppendText(this RichTextBox box, string text, string color)
        {
            BrushConverter bc = new BrushConverter();
            TextRange tr = new TextRange(box.Document.ContentEnd, box.Document.ContentEnd);
            tr.Text = text;
            try
            {
                tr.ApplyPropertyValue(TextElement.ForegroundProperty,
                    bc.ConvertFromString(color));
            }
            catch (FormatException) { }
        }

        public static void SetRtf(this RichTextBox rtb, string document)
        {
            if (document == null)
                return;
            var documentBytes = Encoding.UTF8.GetBytes(document);
            using (var reader = new MemoryStream(documentBytes))
            {
                reader.Position = 0;
                rtb.SelectAll();
                try
                {
                    rtb.Selection.Load(reader, DataFormats.Rtf);

                }
                catch
                {
                    rtb.Selection.Load(reader, DataFormats.Text);
                }
                 }
        }



   
}
    public  class RichTextBoxHelper : DependencyObject
    {
        public static string GetDocumentXaml(DependencyObject obj)
        {
            return (string)obj.GetValue(DocumentXamlProperty);
        }

        public static void SetDocumentXaml(DependencyObject obj, string value)
        {
            obj.SetValue(DocumentXamlProperty, value);
        }

        public static readonly DependencyProperty DocumentXamlProperty =
            DependencyProperty.RegisterAttached(
                "DocumentXaml",
                typeof(string),
                typeof(RichTextBoxHelper),
                new FrameworkPropertyMetadata
                {
                    BindsTwoWayByDefault = true,
                    PropertyChangedCallback = (obj, e) =>
                    {
                        var richTextBox = (RichTextBox)obj;

                        // Parse the XAML to a document (or use XamlReader.Parse())
                        var xaml = GetDocumentXaml(richTextBox);
                        var doc = new FlowDocument();
                        var range = new TextRange(doc.ContentStart, doc.ContentEnd);

                        range.Load(new MemoryStream(Encoding.UTF8.GetBytes(xaml)),
                              DataFormats.Xaml);

                        // Set the document
                        richTextBox.Document = doc;

                        // When the document changes update the source
                        range.Changed += (obj2, e2) =>
                        {
                            if (richTextBox.Document == doc)
                            {
                                MemoryStream buffer = new MemoryStream();
                                range.Save(buffer, DataFormats.Rtf);
                                SetDocumentXaml(richTextBox,
                                    Encoding.UTF8.GetString(buffer.ToArray()));
                            }
                        };
                    }
                });
    }
}
