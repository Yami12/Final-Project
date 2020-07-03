using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
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
        public ObservableCollection<test> tests1 { get; set; }
        public ObservableCollection<test> tests2 { get; set; }

        public Data data { get; set; }

        public MainWindow()
        {
            tests1 = new ObservableCollection<test>();
            tests2 = new ObservableCollection<test>();
            
            tests1.Add(new test() { name = "1234" });
            tests1.Add(new test() { name = "5678" });
            tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" }); tests1.Add(new test() { name = "5678" });
            tests2.Add(new test() { name = "1111" });
            tests2.Add(new test() { name = "2222" });
            data = new Data();
            
            InitializeComponent();
            
            
            data.fPlaylist = new ObservableCollection<FPlTest>();
            DataContext = data;
            ctestListView.ItemsSource = data.cTests;
            //ftestListView.ItemsSource = data.fTests.se(x=> x.test["name"].Split(':')[0] == featuresListView.SelectedItem.ToString());
            playlistListView.ItemsSource = data.fPlaylist;
            

            //mainListView.SelectedIndex = 0;
        }

        private void Btn1_Click(object sender, RoutedEventArgs e)
        {
            
             //run_cmd(@"C:\Users\israel\Downloads\code.py" ,txtb.Text);


        }


        private void run_cmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python.exe";
            start.Arguments = string.Format("{0} {1}", cmd ,args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.CreateNoWindow = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                   // txt1.Text = result;
                }
            }
        }


        private void ListViewItem_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            MessageBox.Show("dsdfsdfsd");
        }

        private void Button_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {

        }

        private void FtestListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if(ftestListView.SelectedItem != null && ((FTest)ftestListView.SelectedItem).supportedApps.Count == 0)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem);
        }

        private void AppsListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if(ftestListView.SelectedItem != null)
                data.UpdatePlaylist((FTest)ftestListView.SelectedItem);
            


        }

     

        private void FDeviceComboBox_GotFocus(object sender, RoutedEventArgs e)
        {
            //ProcessStartInfo start = new ProcessStartInfo();
            //start.FileName = "cmd.exe";
            //start.Arguments = string.Format("{0} {1}", "adb", "devices");
            //start.UseShellExecute = false;
            //start.RedirectStandardOutput = true;
            //start.CreateNoWindow = true;
            
            //using (Process process = Process.Start(start))
            //{
            //    using (StreamReader reader = process.StandardOutput)
            //    {
            //        string result = reader.ReadLine();
            //        txtOutput.Text = result;
            //    }
            //}
        }

        private void FeaturesListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            data.featureTests.Filter = (item) => { return (item as FTest).test["name"].Split(':')[0] == (string)featuresListView.SelectedItem ? true : false; };
            
        }
    }

    public class test
    {
        public string name{ get; set; }
    }
}
