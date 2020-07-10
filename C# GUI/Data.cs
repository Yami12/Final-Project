using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;
using System.Xml.Linq;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows.Data;
using System.Runtime.CompilerServices;
using System.Windows;
using System.Globalization;

namespace Keepers_Automation
{
    public class Data : INotifyPropertyChanged
    {
        public Data()
        {

            fPlaylist = new ObservableCollection<PlaylistItem>();
            cPlaylist = new ObservableCollection<PlaylistItem>();

            cTests = new ObservableCollection<XMLItem>(loadFromXML(COMPONETS_XML_PATH));
            fTests = new ObservableCollection<FTest>(loadFromXML(FEATURE_XML_PATH).ConvertAll(x=> new FTest(x.details)));
            supportedApps = new ObservableCollection<XMLItem>(loadFromXML(APPS_XML_PATH));


        }

        
        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        
        const string FEATURE_XML_PATH = "xml_files\\features_tests.xml";
        const string COMPONETS_XML_PATH = "xml_files\\components_behavior_tests.xml";
        const string APPS_XML_PATH = "xml_files\\applications.xml";
        const string MAIL_XML_PATH = "xml_files\\mail.xml";

        //get / set the mail adress
        public string mail { get { return XElement.Load(System.AppDomain.CurrentDomain.BaseDirectory + MAIL_XML_PATH).Value; } set { new XElement("mail", value).Save(System.AppDomain.CurrentDomain.BaseDirectory + MAIL_XML_PATH); OnPropertyChanged("mail"); } }

        public ObservableCollection<FTest> fTests { get; set; }
        public ObservableCollection<XMLItem> cTests { get; set; }

        private ObservableCollection<XMLItem> _supportedApps;
        public ObservableCollection<XMLItem> supportedApps { get => _supportedApps; set { _supportedApps = value; OnPropertyChanged(); } }

        public HashSet<string> featuresList { get { return fTests.ToList().ConvertAll(x => x.details["name"].ToString().Split(':')[0]).ToHashSet(); } }
        public ICollectionView featureTests { get { return CollectionViewSource.GetDefaultView(fTests); } }


        private ObservableCollection<PlaylistItem> _fPlaylist;
        public ObservableCollection<PlaylistItem> fPlaylist { get => _fPlaylist; set { _fPlaylist = value; OnPropertyChanged(); } }
        private ObservableCollection<PlaylistItem> _cPlaylist;
        public ObservableCollection<PlaylistItem> cPlaylist { get => _cPlaylist; set { _cPlaylist = value; OnPropertyChanged(); } }


        private ObservableCollection<string> _devices;
        public ObservableCollection<string> devices { get { return _devices; } set { _devices = value; OnPropertyChanged(); } }


        /// <summary>
        /// convert the choosen test / app to testViewer format
        /// </summary>
        /// <param name="xmlItem"></param>
        /// <returns></returns>
        public ObservableCollection<TestViewerItem> EditTestViewerItems(XMLItem xmlItem)
        {
            ObservableCollection<TestViewerItem> testViewerItems = new ObservableCollection<TestViewerItem>();

            foreach (var dt in xmlItem.details)
            {

                if (dt.Key == "name")
                    testViewerItems.Add(new TestViewerItem() { key = dt.Key, value = xmlItem.name, isOptional = false, isShowen = true, isReadOnly = false });
                else if(dt.Value != null && dt.Value.GetType() == typeof(List<Dictionary<string, object>>)) //steps
                {
                    var StepsTvi = new TestViewerItem() { key = dt.Key,value= new ObservableCollection<TestViewerItem>(), isOptional = false, isReadOnly = true, isShowen = true };
                    foreach(var step in (List<Dictionary<string, object>>)dt.Value) //step 
                    {
                        var StepTvi = new TestViewerItem() { key = "step", value = new ObservableCollection<TestViewerItem>(), isOptional = true, isReadOnly = true, isShowen = true };
                        foreach (var de in step) //step detalis
                        {
                            ((ObservableCollection<TestViewerItem>)StepTvi.value).Add(new TestViewerItem() { key = de.Key, value = de.Value, isOptional = false, isReadOnly = false, isShowen = true });
                        }
                        ((ObservableCollection<TestViewerItem>)StepsTvi.value).Add(StepTvi);
                    }
                    testViewerItems.Add(StepsTvi);



                }
                else
                    testViewerItems.Add(new TestViewerItem() { key = dt.Key, value = dt.Value, isOptional = false, isShowen = true, isReadOnly = false });
            }
            
            return testViewerItems;
        }

        /// <summary>
        /// convert the edited / addeed test / app  testViewer format to dictinary
        /// </summary>
        /// <param name="testViewrItems"></param>
        /// <returns></returns>
        public Dictionary<string,object> ConvertTestViewrItemsToXmlItem(ObservableCollection<TestViewerItem> testViewrItems)
        {
            Dictionary<string, object> dictionary = new Dictionary<string, object>();
            foreach(var tvi in testViewrItems)
            {

                if(tvi.value != null&& tvi.value.GetType() == typeof(ObservableCollection<TestViewerItem>)) // steps
                {
                    var listSteps = new List<Dictionary<string, object>>();
                    foreach(var step in tvi.value as ObservableCollection<TestViewerItem>) //step
                    {
                        var dictStep = new Dictionary<string, object>();
                        //var listStep = new List<Dictionary<string, object>>();
                        foreach(var dt in step.value as ObservableCollection<TestViewerItem>) // step detalis
                        {
                            dictStep.Add(dt.key, dt.value);
                            //listSteps.Add(new Dictionary<string, object>() { [dt.key] = dt.value });
                        }
                        listSteps.Add(dictStep);

                    }
                    dictionary.Add(tvi.key, listSteps);

                }
                else
                {
                    dictionary.Add(tvi.key, tvi.value);
                }
            }


            return dictionary;
        }
        
        /// <summary>
        /// update the features playlist
        /// </summary>
        /// <param name="fTest"></param>
        public void UpdatePlaylist(FTest fTest)
        {


            if (fTest.supportedApps.Count == 0) //test without supported apps
                if (fPlaylist.Any(x => x.name == fTest.name)) fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name)); else fPlaylist.Add(new PlaylistItem() { name = fTest.name,appName = "Keepers" });
            foreach (var app in fTest.supportedApps)
            {
                if (fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name) && !app.IsSelected)
                    fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name && x.appName == app.name));
                else if (!fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name) && app.IsSelected)
                    fPlaylist.Add(new PlaylistItem() { name = fTest.name, appName = app.name });


            }

        }

        /// <summary>
        /// update the components playlist
        /// </summary>
        public void UpdateCPlaylist()
        {

            foreach (var ct in cTests)
            {
                if (ct.IsSelected && !cPlaylist.Any(x => x.name == ct.name))
                    cPlaylist.Add(new PlaylistItem() { name = ct.name });
                else if (!ct.IsSelected && cPlaylist.Any(x => x.name == ct.name))
                    cPlaylist.Remove(cPlaylist.First(x => x.name == ct.name));


            }


        }


        /// <summary>
        /// load the xml file
        /// </summary>
        /// <param name="path"></param>
        /// <returns></returns>
        public List<XMLItem> loadFromXML(string path)
        {

            XDocument xdoc = XDocument.Load(System.AppDomain.CurrentDomain.BaseDirectory + path);

            List<XMLItem> xmlItems = new List<XMLItem>();
            foreach (var lv1 in xdoc.Root.Elements()) // test
            {
                XMLItem xmlItem = new XMLItem() { details = new Dictionary<string, object>() };
                foreach (var lv2 in lv1.Elements()) // test detailes
                {
                    object value;
                    if (lv2.HasElements)//steps
                    {
                        value = new List<Dictionary<string, object>>();
                        foreach (var lv3 in lv2.Elements()) // step detailes
                        {
                            ((List<Dictionary<string, object>>)value).Add(lv3.Elements().ToDictionary(x => x.Name.LocalName, x => (object)x.Value));
                        }
                    }
                    else
                        value = lv2.Value;
                    xmlItem.details.Add(lv2.Name.LocalName, value);
                }
                xmlItems.Add(xmlItem);
            }
            return xmlItems;

        }

        /// <summary>
        /// save to the xml file
        /// </summary>
        /// <param name="type"></param>
        public void SaveToXML(DetalisType type)
        {
            string rootName ="";
            List<XMLItem> xmlItems = new List<XMLItem>(); 
            string path ="";
            switch (type)
            {
                case DetalisType.cTest:
                    rootName = "tests";
                    xmlItems = cTests.ToList();
                    path = COMPONETS_XML_PATH;
                    break;
                case DetalisType.fTest:
                    rootName = "tests";
                    xmlItems = new List<XMLItem>(fTests.ToList());
                    path = FEATURE_XML_PATH;
                    break;
                case DetalisType.app:
                    rootName = "apps";
                    xmlItems = supportedApps.ToList();
                    path = APPS_XML_PATH;
                    break;
            }


            XElement xElement = new XElement(rootName);//tests
            foreach(var test in xmlItems)
            {
                var lv1 = new XElement(rootName.TrimEnd('s'));//test
                foreach(var detail in test.details)
                {
                    var lv2 = new XElement(detail.Key);
                    if(detail.Value != null)
                    {
                        if (detail.Value.GetType() == typeof(List<Dictionary<string, object>>)) //steps
                        {
                            foreach (var step in (List<Dictionary<string, object>>)detail.Value) // step
                            {
                                var lv3 = new XElement("step");
                                lv3.Add(step.Select(de => new XElement(de.Key, de.Value)));
                                lv2.Add(lv3);
                            }

                        }
                        else
                            lv2.Value = detail.Value.ToString();
                    }

                   

                    lv1.Add(lv2);

                    
                    
                }
                xElement.Add(lv1);
               
               
            }
            xElement.Save(System.AppDomain.CurrentDomain.BaseDirectory + path);

        }


    }


    public class FTest : XMLItem
    {
        public FTest(Dictionary<string, object> testXml)
        {
            details = testXml;
         
        }

        new public string name { get { return details["name"].ToString().Split(':')[1]; } }

        public string featureType { get { return details["name"].ToString().Split(':')[0]; } }


        private ObservableCollection<SupportedApp> _supportedApps;
        public ObservableCollection<SupportedApp> supportedApps
        {
            get
            {
                if (details.Keys.Contains("supportedApps"))
                {
                    var list = details["supportedApps"].ToString().Split(' ').ToList();
                    if (_supportedApps == null)
                        _supportedApps = new ObservableCollection<SupportedApp>(list.ConvertAll(x => new SupportedApp() { name = x }));
                    else if (_supportedApps.Count != list.Count)
                    {
                        foreach(var s in list)
                        {
                            if (_supportedApps.All(x => x.name != s))
                                _supportedApps.Add(new SupportedApp() { name = s });
                        }
                    }
                       
                    
                    return _supportedApps;
                }
                    
                else return new ObservableCollection<SupportedApp>();
            }

        }

 
    }

    public  class SupportedApp : XMLItem
    {
         new public string name { get; set; }

    }

    public class XMLItem : INotifyPropertyChanged
    {
        public string name { get { return details["name"].ToString(); } }

        private Dictionary<string, object> _details;
        public Dictionary<string, object> details { get => _details; set { _details = value;  OnPropertyChanged("name"); OnPropertyChanged("supportedApps"); } }

        public bool IsSelected { get; set; }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }

    public class PlaylistItem : INotifyPropertyChanged
    {


        public string name { get; set; }
        public string appName { get; set; }

        private Status? _status = null;
        public Status? status { get => _status; set { _status = value; OnPropertyChanged(); } }

        private string _output;
        public string output { get => _output; set { _output = value; OnPropertyChanged(); } }


        private Uri _htmlLink;
        public Uri htmlLink { get => _htmlLink; set { _htmlLink = value; OnPropertyChanged(); } }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }



    public enum Status
    {
        
        WAITING,
        RUNNING,
        PASSED,
        FAILED,
        ERROR,
        CANCELLED


    }

    public enum DetalisType
    {
        fTest,
        cTest,
        app
    }

    /// <summary>
    /// check if the test supported app is exist in the apps list
    /// </summary>
    public class IsAppExistConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            Data data = new Data();
            if (data.supportedApps.Any(x => x.name == (string)value))
                return value;
            else
                return null;

        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// convert bool value to visiblty value
    /// </summary>
    public class BoolToVisibiltyHiddenConverter : IValueConverter
    {
       

        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            bool flag = false;
            if (value is bool)
            {
                flag = (bool)value;
            }
            else if (value is bool?)
            {
                bool? nullable = (bool?)value;
                flag = nullable.HasValue ? nullable.Value : false;
            }
            return (flag ? Visibility.Visible : Visibility.Hidden);
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

}
