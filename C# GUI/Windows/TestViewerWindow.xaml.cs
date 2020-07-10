using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;


namespace Keepers_Automation 
{
    /// <summary>
    /// Interaction logic for TestViewerWindow.xaml
    /// </summary>
    public partial class TestViewerWindow : Window
    {
        public Data data { get; set; }

        public TestViewerWindowViewModel testViewerWindowViewModel = new TestViewerWindowViewModel();

        public TestViewerWindow()   
        {

            data = new Data();
            InitializeComponent();
            DataContext = testViewerWindowViewModel;

        }


        /// <summary>
        /// add new item
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void BtnAdd_Click(object sender, RoutedEventArgs e)
        {
            ((Button)sender).ContextMenu.ItemsSource = ((ObservableCollection<TestViewerItem>)((TestViewerItem)((Button)sender).DataContext).value).Where(x => x.isOptional == true && x.isShowen == false);
            ((Button)sender).ContextMenu.IsOpen = true;
        }

        /// <summary>
        /// add new field to step
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void MenuItem_Click(object sender, RoutedEventArgs e)
        {
            ((TestViewerItem)((MenuItem)sender).Header).isShowen = true;

        }

   
        /// <summary>
        /// remove step
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void BtnRemoveOptional_Click(object sender, RoutedEventArgs e)
        {
            TestViewerItem tvi;
            if (((Button)sender).DataContext.GetType() == typeof(ObservableCollection<TestViewerItem>))
                tvi = ((ObservableCollection<TestViewerItem>)((Button)sender).DataContext).FirstOrDefault(x => x.key == ((TextBlock)((Grid)((Button)sender).Parent).Children[1]).Text);
            else
                tvi = ((TestViewerItem)((Button)sender).DataContext);
            
            tvi.isShowen = false;
  
        }

        /// <summary>
        /// add new step
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnAddStep_Click(object sender, RoutedEventArgs e)
        {
           List<string> stepDetails = new List<string>() { "type", "id", "action", "content" };
           ObservableCollection<TestViewerItem> tvis = new ObservableCollection<TestViewerItem>();
           stepDetails.ForEach(x => tvis.Add(new TestViewerItem() {key = x, isOptional = true,isReadOnly = false, isShowen = true }));
           ((ObservableCollection<TestViewerItem>)((Button)sender).DataContext).Add(new TestViewerItem() { key = "step",value= tvis ,isOptional = true, isShowen = true, isReadOnly = true});
        }

        /// <summary>
        /// save the changes
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            var details = data.ConvertTestViewrItemsToXmlItem(testViewerWindowViewModel.testViewerItems);
            if(testViewerWindowViewModel.source != null)
                testViewerWindowViewModel.source.details = details;
            

            this.DialogResult = true;
            this.Close();
            

        }
    }


    
}
