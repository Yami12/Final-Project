using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace Keepers_Automation
{
    public class TestViewerWindowViewModel : INotifyPropertyChanged
    {

        private ObservableCollection<TestViewerItem> _testViewerItems;
        public ObservableCollection<TestViewerItem> testViewerItems { get => _testViewerItems; set { _testViewerItems = value; OnPropertyChanged(); } }

        public  XMLItem source { get; set; }

        public bool isAdd { get { return testViewerItems.Any(x => x.isOptional == true && x.isShowen == false); } }


        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        
    }

    public class TestViewerItem : INotifyPropertyChanged
    {

        private bool _isShowen;
        private string _key;
        private object _value;
        private bool _isOptional;
        private bool _isReadOnly;
        private bool _isAdd;


        public string key { get => _key; set { _key = value; OnPropertyChanged(); } }
        public object value { get => _value; set { _value = value; OnPropertyChanged(); setIsAdd(); } }

        public bool isOptional { get => _isOptional; set { _isOptional = value; OnPropertyChanged(); } }
        public bool isShowen { get => _isShowen; set { _isShowen = value; OnPropertyChanged(); } }

        public bool isAdd { get => _isAdd; set { _isAdd = value; OnPropertyChanged(); } }
        public bool isReadOnly { get => _isReadOnly; set { _isReadOnly = value; OnPropertyChanged(); } }

        public void setIsAdd()
        {
            if (value is ObservableCollection<TestViewerItem>)
            {
                isAdd = (value as ObservableCollection<TestViewerItem>).Any(x => x.isOptional == true && x.isShowen == false);
                OnPropertyChanged("isAdd");
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

    
    }

    public class MyDataTemplateSelector : DataTemplateSelector
    {
        public override DataTemplate SelectTemplate(object item, DependencyObject container)
        {
            FrameworkElement element = container as FrameworkElement;

            if (element != null && item != null && item is TestViewerItem myItem)
            {

                if(myItem.value!= null&& myItem.value.GetType() == typeof(ObservableCollection<TestViewerItem>))
                    return element.FindResource("listT") as DataTemplate;
                else
                    return element.FindResource("oneT") as DataTemplate;
               
            }

            return element.FindResource("oneT") as DataTemplate; ; // or provide a default template
        }
    }

    
}
