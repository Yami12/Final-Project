using System;
using System.Collections.Generic;
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

namespace Keepers_Automation
{
    /// <summary>
    /// Interaction logic for RichTextBoxDataFormating.xaml
    /// </summary>
    public partial class RichTextBoxDataFormating : UserControl
    {
        public RichTextBoxDataFormating()
        {
            InitializeComponent();
        }



        public string dataFormat
        {
            get { return (string)GetValue(dataFormatProperty); }
            set { SetValue(dataFormatProperty, value); }
        }

        // Using a DependencyProperty as the backing store for dataFormat.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty dataFormatProperty =
            DependencyProperty.Register("dataFormat", typeof(string), typeof(RichTextBoxDataFormating), new PropertyMetadata(DataFormats.Text));



        public string Text
        {
            get { return (string)GetValue(TextProperty); }
            set { SetValue(TextProperty, value); UpdateRtb(); }
        }

        // Using a DependencyProperty as the backing store for Text.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty TextProperty =
            DependencyProperty.Register("Text", typeof(string), typeof(RichTextBoxDataFormating), new PropertyMetadata(string.Empty,new PropertyChangedCallback((Changed))));



        private static void Changed(DependencyObject d ,DependencyPropertyChangedEventArgs e )
        {
            ((RichTextBoxDataFormating)d).UpdateRtb();

        }


        private void UpdateRtb()
        {
            if (Text == null)
                return;
            var documentBytes = Encoding.UTF8.GetBytes(this.Text);
            using (var reader = new MemoryStream(documentBytes))
            {
                reader.Position = 0;
                rtb.SelectAll();
                try
                {
                    rtb.Selection.Load(reader, dataFormat);
                    

                }
                catch
                {
                    rtb.Selection.Load(reader, DataFormats.Text);
                }
            }
        }

    }
}
