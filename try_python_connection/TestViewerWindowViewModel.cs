using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace try_python_connection
{
    public class TestViewerWindowViewModel : INotifyPropertyChanged
    {
        private ObservableCollection<TestViewerItem> _testViewerItems;

        public ObservableCollection<TestViewerItem> testViewerItems { get => _testViewerItems; set { _testViewerItems = value; OnPropertyChanged(); } }

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

        public string key { get => _key; set { _key = value; OnPropertyChanged(); } }
        public object value { get => _value; set { _value = value; OnPropertyChanged(); } }
        public bool isOptional { get => _isOptional; set { _isOptional = value; OnPropertyChanged(); } }
        public bool isShowen { get => _isShowen; set { _isShowen = value; OnPropertyChanged(); } }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}
