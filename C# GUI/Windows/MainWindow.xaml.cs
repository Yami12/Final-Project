
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.Diagnostics;
using System.IO;
using System.Linq;

using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

using System.Windows.Documents;
using System.Windows.Input;


namespace Keepers_Automation
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        private readonly object LockObj = new object();
        private CancellationTokenSource cancellationToken = new CancellationTokenSource();
        private string foldername;
        private string path;
        const string EXE_PATH = "\\keepers_automation.exe";
        private Process process;

        public Data data { get; set; }

        
        public MainWindow()
        {
            InitializeComponent();
            
            data = new Data();
            DataContext = data;
            tabControl.SelectedIndex = 0;
            ((INotifyCollectionChanged)playlistListView.Items).CollectionChanged += playlistListViewCollectionChanged;
            refreshDevices();
        }

        #region Events
        
        //list view...

        /// <summary>
        /// called when there is a changed in the playlist choise
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void playlistListViewCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {

            CheckEnableBtnRun(); // checks if the playlist is not empty
        }

        /// <summary>
        /// called when there is a changed in the features tests list choise
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void FtestListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ftestListView.SelectedItem != null && ((FTest)ftestListView.SelectedItem).supportedApps.Count == 0)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem); // add / remove test to the playlist - if there is no apps supported
        }

        /// <summary>
        ///called when there is a changed in the components tests list choise
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ctestListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            data.UpdateCPlaylist(); // add / remove test to the playlist 
        }

        /// <summary>
        /// called when there is a changed in the apps list choise
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void AppsListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ftestListView.SelectedItem != null)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem); // add / remove test to the playlist

        }


        /// <summary>
        /// called when there is a changed in the features categories choise
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void FeaturesListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // display all the category tests
            data.featureTests.Filter = (item) => { return (item as FTest).details["name"].ToString().Split(':')[0] == (string)featuresListView.SelectedItem ? true : false; };

        }

        /// <summary>
        /// called when double click on the item
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ListViewItem_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {

            var xmlItem = ((sender as ListViewItem).Content as XMLItem);

            string title = "";
            DetalisType type;
            if ((sender as ListViewItem).Content is FTest) // feature test
            {
                xmlItem = ((sender as ListViewItem).Content as FTest);
                title = "Edit " + xmlItem.name + " test";
                type = DetalisType.fTest;
            }
            else if ((sender as ListViewItem).Content is SupportedApp) // app
            {
                SupportedApp supportedApp = ((sender as ListViewItem).Content as SupportedApp);

                xmlItem = data.supportedApps.FirstOrDefault(x => x.name == supportedApp.name);
                title = "Edit " + xmlItem.name + " app";
                type = DetalisType.app;

            }
            else // component test
            {
                title = "Edit " + xmlItem.name + " test";
                type = DetalisType.cTest;
            }


            OpenTestViewrWindow(data.EditTestViewerItems(xmlItem), xmlItem, title); // open the edit window
            data.SaveToXML(type); // save the changes to the xml file
        }


        //buttons click
        /// <summary>
        /// click on run button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void BtnRun_Click(object sender, RoutedEventArgs e)
        {
            run_test(); // run the playlist

        }

        /// <summary>
        /// click on remove button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void BtnRemoveTest_Click(object sender, RoutedEventArgs e)
        {

            if ((sender as Button).DataContext is FTest) // remove feature test
            {
                data.fTests.RemoveAt(data.fTests.IndexOf((FTest)ftestListView.SelectedItem) + 1);
                data.SaveToXML(DetalisType.fTest);
            }

            else if ((sender as Button).DataContext is SupportedApp) // remove app
            {
                data.supportedApps.Remove(data.supportedApps.First(x => x.name == ((sender as Button).DataContext as SupportedApp).name));
                data.SaveToXML(DetalisType.app);
            }

            else if ((sender as Button).DataContext is XMLItem) // remove component test
            {
                data.cTests.Remove((sender as Button).DataContext as XMLItem); 
                data.SaveToXML(DetalisType.cTest);
            }

        }

        /// <summary>
        /// click on refresh devices button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnRefreshDevices_Click(object sender, RoutedEventArgs e)
        {
            refreshDevices();
        }

        /// <summary>
        /// click on stop button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnStop_Click(object sender, RoutedEventArgs e)
        {
            if (process != null)
            {
                cancellationToken.Cancel();
            }

        }

        /// <summary>
        /// click on add new test to components tests
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnAddTest_Click(object sender, RoutedEventArgs e)
        {
            object value = null;
            XMLItem xmlItem = new XMLItem();
            List<string> testDeatils = new List<string>() { "name", "expectedResult", "steps" };
            ObservableCollection<TestViewerItem> tvis = new ObservableCollection<TestViewerItem>();
            testDeatils.ForEach(x => { if (x == "steps") value = new ObservableCollection<TestViewerItem>(); tvis.Add(new TestViewerItem() { key = x, value = value, isOptional = false, isReadOnly = false, isShowen = true }); });

            if (OpenTestViewrWindow(tvis, xmlItem, "Add new test")) // open the new test window
            {
                data.cTests.Add(xmlItem); // add the test
                data.SaveToXML(DetalisType.cTest); // save the changes to the xml file
            }

        }

        /// <summary>
        /// click on add new app
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnAddApp_Click(object sender, RoutedEventArgs e)
        {
            object value = null;
            SupportedApp supportedApp = new SupportedApp();
            List<string> testDeatils = new List<string>() { "name", "app_package", "app_activity", "parent_name", "child_name", "group_name", "steps" };
            ObservableCollection<TestViewerItem> tvis = new ObservableCollection<TestViewerItem>();
            testDeatils.ForEach(x => { if (x == "steps") value = new ObservableCollection<TestViewerItem>(); tvis.Add(new TestViewerItem() { key = x, value = value, isOptional = false, isReadOnly = false, isShowen = true }); });

            if (OpenTestViewrWindow(tvis, supportedApp, "Add new app")) // open the new app window
            {
                data.supportedApps.Add(supportedApp); // add the app
                data.SaveToXML(DetalisType.app); // save the changes to the xml file

            }

        }

        /// <summary>
        /// click on the setting button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSettings_Click(object sender, RoutedEventArgs e)
        {
            SettingsWindow settingsWindow = new SettingsWindow();
            settingsWindow.ShowDialog();
        }



        /// <summary>
        /// click on the send to mail button
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private async void btnMail_Click(object sender, RoutedEventArgs e)
        {
            await run_cmd
                (
                    path,
                    string.Format("{0} {1} {2}", "mail", data.mail, foldername),
                    (s, ev) =>
                    { },
                    (s, ev) =>
                    { }

                );

        }


        //others...
        /// <summary>
        /// choose the devices for features tests
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void DeviceComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ComboBox otherComboBox;
            if (((ComboBox)sender) == fDeviceComboBox)
                otherComboBox = cDeviceComboBox;
            else
                otherComboBox = fDeviceComboBox;


            if (((ComboBox)sender).SelectedItem == otherComboBox.SelectedItem) // checks duplicate choise
                otherComboBox.SelectedIndex = -1;

            if (data.devices != null && data.devices.Count == 2) // if there is just 2 devices auto fill the second device
                switch (((ComboBox)sender).SelectedIndex)
                {
                    case 0:
                        otherComboBox.SelectedIndex = 1;
                        break;
                    case 1:
                        otherComboBox.SelectedIndex = 0;
                        break;
                }


            CheckEnableBtnRun(); // enable the run button


        }

        /// <summary>
        /// choose the device for components tests 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ctDeviceComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            CheckEnableBtnRun(); // enable the run button
        }


        /// <summary>
        /// checked / unchecked all the feature tests
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chbRunAllFtest_Checked(object sender, RoutedEventArgs e)
        {
            bool isChecked = (bool)((sender as CheckBox).IsChecked);

            foreach (var ft in data.fTests)
            {
                foreach (var sa in ft.supportedApps)
                {
                    sa.IsSelected = isChecked;
                }
                ft.IsSelected = isChecked;

                data.UpdatePlaylist(ft); // add to the playlist
            }

        }


        /// <summary>
        /// checked / unchecked all the apps
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void chbRunAllApps_Checked(object sender, RoutedEventArgs e)
        {
            bool isChecked = (bool)((sender as CheckBox).IsChecked);



            foreach (var sa in (ftestListView.SelectedItem as FTest).supportedApps)
            {

                sa.IsSelected = isChecked;


            }
            data.UpdatePlaylist((ftestListView.SelectedItem as FTest)); // add to playlist
        }

        /// <summary>
        /// checked / unchecked all the components tests
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ChbRunAllCtest_Checked(object sender, RoutedEventArgs e)
        {
            bool isChecked = (bool)((sender as CheckBox).IsChecked);

            foreach (var ct in data.cTests)
            {

                ct.IsSelected = isChecked;

                data.UpdateCPlaylist(); // add to the playlist
            }
        }

        /// <summary>
        /// display features playlist or components playlist
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void tabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

            if ((tabControl.SelectedItem as TabItem).Header.ToString() == "Features")
                playlistListView.ItemsSource = data.fPlaylist;
            else if (((tabControl.SelectedItem as TabItem).Header.ToString() == "Components"))
                playlistListView.ItemsSource = data.cPlaylist;
        }

        /// <summary>
        /// link to the test result html file
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void link_Click(object sender, RoutedEventArgs e)
        {
            if ((e.OriginalSource as Hyperlink).NavigateUri != null && File.Exists((e.OriginalSource as Hyperlink).NavigateUri.LocalPath))
                Process.Start((e.OriginalSource as Hyperlink).NavigateUri.LocalPath);
        }

        //window
        /// <summary>
        /// close all the threads on exit
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private async void Window_Closed(object sender, EventArgs e)
        {
            System.Windows.Application.Current.ShutdownMode = ShutdownMode.OnExplicitShutdown;
            System.Windows.Application.Current.Shutdown();
            await run_cmd("cmd.exe", "/c taskkill /F /IM node.exe", null, null); // close appium
            
        }

        /// <summary>
        /// open appium on load
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private async void Window_Loaded(object sender, RoutedEventArgs e)
        {
            
            await run_cmd("cmd.exe", "/C appium", (s, ev) => { Debug.WriteLine(ev.Data); }, (s, ev) => { Debug.WriteLine(ev.Data); });


        }
        #endregion




        #region function

        /// <summary>
        /// open new process to run a test, open appium, open adb, send a mail 
        /// </summary>
        /// <param name="cmd"></param>
        /// <param name="args"></param>
        /// <param name="OutputDataReceivedEventHandler"></param>
        /// <param name="ErorrDataReceivedEventHandler"></param>
        /// <returns></returns>
        private async Task<int> run_cmd(string cmd, string args, DataReceivedEventHandler OutputDataReceivedEventHandler, DataReceivedEventHandler ErorrDataReceivedEventHandler)
        {


            int i;

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
                Verb = "runas"

            };

            process = Process.Start(StartInfo);
            var name = process.ProcessName;
            process.OutputDataReceived += OutputDataReceivedEventHandler;
            process.ErrorDataReceived += ErorrDataReceivedEventHandler;
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            await Task.Run(() =>
            {
                while (!process.HasExited && !cancellationToken.IsCancellationRequested) // the proccess is runing and there is no cancell request
                {

                }
            }
            );

            if (process.HasExited) // the process finished
            {
                i = process.ExitCode; // save the exit code
               
            }
                
            else // cancellation
            {
                i = 2; // cancel status
                foreach (var p in Process.GetProcessesByName(name))
                {
                    p.Kill();
                }

            }

            return i;

        }

        /// <summary>
        /// run playlist
        /// </summary>
        private async void run_test()
        {
            //disable GUI
            btnMail.IsEnabled = false;
            tabControl.IsEnabled = false;
            btnRun.Visibility = Visibility.Collapsed;

            //get type
            DetalisType type = DetalisType.cTest;
            if (tabControl.SelectedIndex == 0)
                type = DetalisType.fTest;

            //set 
            path = System.AppDomain.CurrentDomain.BaseDirectory + EXE_PATH;
            foldername = "test_" + DateTime.Now.Millisecond;
            ObservableCollection<PlaylistItem> playlist = playlistListView.ItemsSource as ObservableCollection<PlaylistItem>;
            string param = "";

            foreach (var test in playlist)
            {
                test.status = Status.WAITING;
                test.output = "";
                test.htmlLink = null;
            }



            //start
            foreach (var fp in playlist)
            {
                if (type == DetalisType.fTest)
                    param = string.Format("{0} {1} {2} {3} {4} {5}", "f", "\"" + fp.name + "\"", fp.appName, fDeviceComboBox.SelectedItem, cDeviceComboBox.SelectedItem, foldername);
                else if (type == DetalisType.cTest)
                    param = string.Format("{0} {1} {2} {3}", "c", "\"" + fp.name + "\"", ctDeviceComboBox.SelectedItem, foldername);

                playlistListView.SelectedItem = fp;
                fp.status = Status.RUNNING;

                int exitCode = await run_cmd
                (
                    path,
                    param,
                    (s, ev) =>
                    {
                        lock (LockObj)
                        {
                            fp.output += (ev.Data); //get the std output
                        }

                    },
                    (s, ev) =>
                    {
                        lock (LockObj)
                        {
                            fp.output += ("\\line \\cf2" + ev.Data + "\\line"); // get the stderr output
                        }
                    }

                );


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
                    case 2:
                        fp.status = Status.CANCELLED;
                        break;


                }

                //stop 
                if (cancellationToken.IsCancellationRequested)
                {
                    cancellationToken = new CancellationTokenSource();
                    tabControl.IsEnabled = true;
                    btnRun.Visibility = Visibility.Visible;
                    return;
                }
                //html file link
                fp.htmlLink = new Uri(System.AppDomain.CurrentDomain.BaseDirectory + "tests_results\\" + foldername + @"\" + fp.name + ".html");
            }

            //enable GUI
            tabControl.IsEnabled = true;
            btnRun.Visibility = Visibility.Visible;
            btnMail.IsEnabled = true;
        }

        /// <summary>
        /// edit/ add test / app
        /// </summary>
        /// <param name="testViewerItems"></param>
        /// <param name="source"></param>
        /// <param name="title"></param>
        /// <returns></returns>
        private bool OpenTestViewrWindow(ObservableCollection<TestViewerItem> testViewerItems, XMLItem source, string title)
        {
            var testViewerWindow = new TestViewerWindow();
            testViewerWindow.Title = title;
            testViewerWindow.testViewerWindowViewModel.testViewerItems = testViewerItems;
            testViewerWindow.testViewerWindowViewModel.source = source;
            testViewerWindow.ShowInTaskbar = false;
            testViewerWindow.Owner = this;

            if (testViewerWindow.ShowDialog() == true)
            {
                source = testViewerWindow.testViewerWindowViewModel.source;
                return true;
            }
            return false;

        }

        /// <summary>
        /// refresh the connected devices list
        /// </summary>
        private async void refreshDevices()
        {
            btnRefreshDevices.IsEnabled = false;

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
                    (s, ev) => { }

                );
            btnRefreshDevices.IsEnabled = true; ;
        }

        /// <summary>
        /// check if the run button is enabled
        /// </summary>
        private void CheckEnableBtnRun()
        {

            if ((tabControl.SelectedIndex == 0 && fDeviceComboBox.SelectedIndex != -1 && cDeviceComboBox.SelectedIndex != -1 && data.fPlaylist.Count > 0)
                || (tabControl.SelectedIndex == 1 && ctDeviceComboBox.SelectedIndex != -1 && data.cPlaylist.Count > 0))
                btnRun.IsEnabled = true;
            else
                btnRun.IsEnabled = false;
        }
        #endregion


       
    }

}
