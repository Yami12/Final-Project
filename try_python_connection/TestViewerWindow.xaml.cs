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


namespace try_python_connection 
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

            
            InitializeComponent();
            DataContext = testViewerWindowViewModel;
            
           

        }

       

        private void BtnAdd_Click(object sender, RoutedEventArgs e)
        {
            //btnAdd.ContextMenu = new ContextMenu();
            btnAdd.ContextMenu.ItemsSource = testViewerWindowViewModel.testViewerItems.Where(x=> x.isOptional == true && x.isShowen == false);
            
            btnAdd.ContextMenu.IsOpen = true;
        }

        private void MenuItem_Click(object sender, RoutedEventArgs e)
        {
            var tvi = testViewerWindowViewModel.testViewerItems.FirstOrDefault(x => x.key == ((TestViewerItem)((MenuItem)sender).Header).key);
            tvi.isShowen = true;
       
        }

   

        private void BtnRemoveOptional_Click(object sender, RoutedEventArgs e)
        {
            var tvi = testViewerWindowViewModel.testViewerItems.FirstOrDefault(x => x.key == ((TextBlock)((Grid)((Button)sender).Parent).Children[1]).Text);
            tvi.isShowen = false;
             
        }
    }


    
}
