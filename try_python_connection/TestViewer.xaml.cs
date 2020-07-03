using System;
using System.Collections.Generic;
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
    /// Interaction logic for TestViewer.xaml
    /// </summary>
    public partial class TestViewer : UserControl
    {
        public TestViewer()
        {
            InitializeComponent();
   
        }

        public void displayDetail(string key, string value, bool IsNecessary)
        {

            Grid grid = new Grid();
            grid.ColumnDefinitions.Add(new ColumnDefinition());
            grid.ColumnDefinitions.Add(new ColumnDefinition());

            if (!IsNecessary)
            {
                StackPanel stackPanel = new StackPanel();
                Button button = new Button();
                
            }
                

            TextBlock textBlock = new TextBlock() { Text = key, Margin = new Thickness(2) };
            grid.Children.Add(textBlock);
            Grid.SetColumn(textBlock,0);
            TextBox textBox = new TextBox() { Text = value, Margin = new Thickness(2) };
            grid.Children.Add(textBox);
            Grid.SetColumn(textBox, 1);

            stMain.Children.Add(grid);
        }




        public Dictionary<string, string> necessaryDetails
        {
            get { return (Dictionary<string, string>)GetValue(necessaryDetailsProperty); }
            set {
                    SetValue(necessaryDetailsProperty, value);
                    foreach (var nd in necessaryDetails)
                    {
                        displayDetail(nd.Key, nd.Value,true);
                    }
                }
        }

        // Using a DependencyProperty as the backing store for necessaryDetails.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty necessaryDetailsProperty =
            DependencyProperty.Register("necessaryDetails", typeof(Dictionary<string, string>), typeof(TestViewer), new PropertyMetadata(new Dictionary<string,string>()));



        //public Dictionary<string, string> necessaryDetails { get; set; } = new Dictionary<string, string>();



        public Dictionary<string, string> optionalDetailsShowen
        {
            get { return (Dictionary<string, string>)GetValue(optionalDetailsShowenProperty); }
            set
            {
                if (value.Count > optionalDetailsShowen.Count)
                    displayDetail(value.Last().Key, value.Last().Value, false);
                SetValue(optionalDetailsShowenProperty, value);
                
            }
        }

        // Using a DependencyProperty as the backing store for MyProperty.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty optionalDetailsShowenProperty =
            DependencyProperty.Register("optionalDetailsShowen", typeof(Dictionary<string, string>), typeof(TestViewer), new PropertyMetadata(new Dictionary<string, string>()));

        public Dictionary<string, string> optionalDetailsUnShowen
        {
            get { return (Dictionary<string, string>)GetValue(optionalDetailsUnShowenProperty); }
            set { SetValue(optionalDetailsUnShowenProperty, value); if (value.Count > 0) btnAdd.Visibility = Visibility.Visible; else btnAdd.Visibility = Visibility.Collapsed; }
        }

        // Using a DependencyProperty as the backing store for MyProperty.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty optionalDetailsUnShowenProperty =
            DependencyProperty.Register("optionalDetailsUnShowen", typeof(Dictionary<string, string>), typeof(TestViewer), new PropertyMetadata(new Dictionary<string, string>()));



        //public Dictionary<string, string> optionalDetails { get; set; }


    }
}
