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

namespace try_python_connection
{
    public class Data : INotifyPropertyChanged
    {
        public Data()
        {



            cTests = new ObservableCollection<CTest>(loadCtestsFromXML());
            fTests = new ObservableCollection<FTest>(loadFtestsFromXML());

            //SaveToXML("tests", fTests.ToList().ConvertAll(x => x.details));
            //SaveToXML("tests","test", cTests.ToList().ConvertAll(x => x.details));

            //loadAppsFromXML();
            //nd = fTests[0].test;
            fTestViewerItems = newFtestViewerItems();
            devices = new ObservableCollection<string>();

        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        const string FEATURE_XML_PATH = "/xml files\\feature_tests.xml";
        const string COMPONETS_XML_PATH = "/xml files\\components_behavior_tests.xml";
        const string APPS_XML_PATH = "/xml files\\apps.xml";

        public List<string> fTestNecessaryDetails { get { return new List<string>() { "name" }; } }
        public List<string> fTestOptionalDetails { get { return new List<string>() { "supportedApps", "groupName", "website_address" }; } }


        public ObservableCollection<TestViewerItem> fTestViewerItems { get; set; }
        public ObservableCollection<TestViewerItem> cTestViewerItems { get; set; }

        public ObservableCollection<TestViewerItem> newFtestViewerItems()
        {
            ObservableCollection<TestViewerItem> testViewerItems = new ObservableCollection<TestViewerItem>();

            fTestNecessaryDetails.ForEach(x => testViewerItems.Add(new TestViewerItem() { key = x, isOptional = false, isShowen = true }));
            fTestOptionalDetails.ForEach(x => testViewerItems.Add(new TestViewerItem() { key = x, isOptional = true }));

            return testViewerItems;
        }
        //public ObservableCollection<TestViewerItem> editCtestViewerItems(CTest cTest)
        //{
        //    ObservableCollection<TestViewerItem> testViewerItems = new ObservableCollection<TestViewerItem>();

        //    foreach (var d in cTest.details)
        //    {
        //        TestViewerItem testViewerItem = new TestViewerItem() { key = d.Key };

        //        if (d.Value.GetType() == typeof(List<Dictionary<string, string>>))
        //        {
        //            var tviList = new List<TestViewerItem>();
        //            foreach (var l in ((List<Dictionary<string, string>>)d.Value))
        //            {
        //                tviList.Add(new TestViewerItem() { key =})
        //            }
        //            ((List<Dictionary<string, string>>)d.Value).ConvertAll(x => new List<TestViewerItem>() { new TestViewerItem() { key = x.} })
        //        }

        //        testViewerItems.Add(testViewerItem);
        //    }

        //    return testViewerItems;
        //}


        public ObservableCollection<FTest> fTests { get; set; }

        public HashSet<string> featuresList { get { return fTests.ToList().ConvertAll(x => x.details["name"].ToString().Split(':')[0]).ToHashSet(); } }
        public ICollectionView featureTests { get { return CollectionViewSource.GetDefaultView(fTests); } }


        public ObservableCollection<CTest> cTests { get; set; }

        

        private ObservableCollection<PlaylistItem> _fPlaylist;
        public ObservableCollection<PlaylistItem> fPlaylist { get => _fPlaylist; set { _fPlaylist = value;  OnPropertyChanged();  } }

        public ObservableCollection<PlaylistItem> cPlaylist { get; set; }


        private string _output;
        public string output { get { return _output; } set { _output = value; OnPropertyChanged(); } }



        public int currentTest { get; set; }

        private ObservableCollection<string> _devices;
        

        public ObservableCollection<string> devices { get { return _devices; } set { _devices = value; OnPropertyChanged(); } }

        public ICollectionView fdevices { get { return CollectionViewSource.GetDefaultView(devices); } }

        public void UpdatePlaylist(FTest fTest)
        {
            if (fTest.supportedApps.Count == 0) //test without supported apps
                if (fPlaylist.Any(x => x.name == fTest.name)) fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name)); else fPlaylist.Add(new PlaylistItem() { name = fTest.name });
            foreach (var app in fTest.supportedApps)
            {
                if (fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name) && !app.IsSelected)
                    fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name && x.appName == app.name));
                else if (!fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name) && app.IsSelected)
                    fPlaylist.Add(new PlaylistItem() { name = fTest.name, appName = app.name });


            }

        }

        public List<CTest> loadCtestsFromXML()
        {

            XDocument xdoc = XDocument.Load(System.AppDomain.CurrentDomain.BaseDirectory + COMPONETS_XML_PATH);
            //var listTest = new List<CTest>();
            //foreach(var xe in xdoc.Descendants("test"))
            //{
            //    var dict = convertXMLelemtToDict(xe, new Dictionary<string, object>());
            //    listTest.Add(new CTest() { details = dict });
            //}
            //return listTest;







            List<CTest> cTests = new List<CTest>();
            foreach (var lv1 in xdoc.Root.Elements())
            {
                CTest ctest = new CTest() { details = new Dictionary<string, object>() };
                foreach (var lv2 in lv1.Elements())
                {
                    object value;
                    if (lv2.HasElements)
                    {
                        value = new List<Dictionary<string, object>>();
                        foreach (var lv3 in lv2.Elements())
                        {
                            ((List<Dictionary<string, object>>)value).Add(lv3.Elements().ToDictionary(x => x.Name.LocalName, x => (object)x.Value));
                        }
                    }
                    else
                        value = lv2.Value;
                    ctest.details.Add(lv2.Name.LocalName, value);
                }
                cTests.Add(ctest);
            }
            return cTests;

        }

        public List<FTest> loadFtestsFromXML()
        {
            XDocument xdoc = XDocument.Load(System.AppDomain.CurrentDomain.BaseDirectory + FEATURE_XML_PATH);

            //var listTest = new List<FTest>();
            //foreach (var xe in xdoc.Descendants("test"))
            //{
            //    var dict = convertXMLelemtToDict(xe, new Dictionary<string, object>());
            //    listTest.Add(new FTest(dict));
            //}
            //return listTest;

            var ldict = from lv1 in xdoc.Descendants("test")
                        select new FTest(lv1.Descendants().ToDictionary(x => x.Name.LocalName, x => (object)x.Value));


            return ldict.ToList();

        }

        public void SaveToXML(string title, string subTitle, List<Dictionary<string, object>> dictList)
        {
            Dictionary<string, object> ddd = new Dictionary<string, object>();

            XElement xElement = new XElement(title);
            XElement xElement1 = new XElement(subTitle);
            //foreach (var dict in dictList)
            //{
            //    foreach(var dict2 in dict)
            //    {
            //        xElement1 = convertXMLelemtToDict2(dict2, xElement1);
            //    }
            //    xElement.Add(xElement1);
            //}
            dictList.ForEach(l => l.ToList().ForEach(d => { xElement = convertXMLelemtToDict2(d, xElement, subTitle); }));
            //xElement.Add(xElement1);
            //xElement = convertXMLelemtToDict2(dict, xElement);

            //foreach(var ft in fTests)
            //{
            //    xElement.Add(new XElement("test"));
            //    foreach (var t in ft.details)
            //    {
            //        Debug.WriteLine(t.Key.ToString() + "        " + t.Value);
            //        xElement.Elements().LastOrDefault(x=> x.Name == "test").Add(new XElement(t.Key.ToString(), t.Value));
            //    }

            //}

            //foreach (var e in xElement.Elements())
            //    Debug.WriteLine(e.Name + "    -----    " + e.Value);





            xElement.Save(@"D:\try_python_connection\try_python_connection\xml files\feature_tests2.xml");




        }

        //public List<Dictionary<string, object>> loadAppsFromXML()
        //{

        //    XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\apps.xml");
        //    var appsList = new List<Dictionary<string, object>>();
        //    foreach(var des in xdoc.Descendants("app").Elements())
        //    {
        //        var app = new Dictionary<string, object>();
        //        if (des.HasElements)
        //            app.Add(des.Name.LocalName, new List<Dictionary<string, object>>().Append(des.Descendants(des.Name.LocalName).Descendants().ToDictionary(x => x.Name.LocalName, x => (object)x.Value)));
        //        else
        //            app.Add(des.Name.LocalName, des.Value);
        //    }
        //    return appsList;

        //}




        public Dictionary<string, object> convertXMLelemtToDict(XElement xElement, Dictionary<string, object> parentDict)
        {

            Dictionary<string, object> dict = new Dictionary<string, object>();
            List<Dictionary<string, object>> dictList = new List<Dictionary<string, object>>();
            if (!xElement.HasElements)
            {

                parentDict.Add(xElement.Name.LocalName, xElement.Value);
                return parentDict;
            }
            else if (xElement.Name.LocalName == "steps")
            {

                foreach (var x in xElement.Elements("step"))
                    dictList.Add(new Dictionary<string, object>() { ["step"] = x.Elements().ToDictionary(k => k.Name.LocalName, v => (object)v.Value) });

                parentDict.Add(xElement.Name.LocalName, dictList);
                return parentDict;
            }
            else
            {
                foreach (var x in xElement.Elements())
                {
                    if (xElement.Name.LocalName == "steps")
                    {

                        foreach (var x1 in xElement.Elements("step"))
                            dictList.Add(new Dictionary<string, object>() { ["step"] = x1.Elements().ToDictionary(k => k.Name.LocalName, v => (object)v.Value) });

                        parentDict.Add(xElement.Name.LocalName, dictList);

                    }
                    else
                    {
                        parentDict.Add(x.Name.LocalName, x.Value);
                    }

                }
                //    dict.Add(x.Name.LocalName,convertXMLelemtToDict(x, new Dictionary<string, object>()));
                //parentDict.Add(xElement.Name.LocalName,dictList);
                return parentDict;
            }


        }

        public XElement convertXMLelemtToDict2(KeyValuePair<string, object> detail, XElement parentXElement, string title)
        {

            Dictionary<string, object> dict = new Dictionary<string, object>();
            if (detail.Value.GetType() == typeof(string))
            {

                parentXElement.Add(detail.Key, detail.Value);
                return parentXElement;
            }
            else if (detail.Key == "steps")
            {
                List<XElement> elementsLv1 = new List<XElement>();
                foreach (var step in (List<Dictionary<string, object>>)detail.Value)
                {
                    List<XElement> elementsLv2 = new List<XElement>();
                    foreach (var d in step)
                    {
                        elementsLv2.Add(new XElement(d.Key, d.Value));
                    }
                    var xe = new XElement("step");
                    xe.Add(elementsLv2);
                    elementsLv1.Add(xe);

                }
                parentXElement.Add(elementsLv1);
                return parentXElement;
                //List<Dictionary<string, object>> dictList = new List<Dictionary<string, object>>();
                //foreach (var x in xElement.Elements("step"))
                //    dictList.Add(x.Elements().ToDictionary(k => k.Name.LocalName, v => (object)v.Value));
                //parentDict.Add(xElement.Name.LocalName, dictList);
                //return parentDict;
            }
            else
            {
                List<XElement> elementsLv1 = new List<XElement>();
                foreach (var v in (Dictionary<string, object>)detail.Value)
                {
                    elementsLv1.Add(new XElement(v.Key, v.Value));
                }
                var xe = new XElement(detail.Key);
                var xe1 = new XElement(title);
                xe.Add(elementsLv1);
                xe1.Add(xe);
                parentXElement.Add(xe1);
                return parentXElement;
                //parentDict.Add(xElement.Name.LocalName, xElement.Elements().ToDictionary(k => k.Name.LocalName, v => (object)v.Value));
                //return parentDict;
            }


        }




    }



    public class FTest
    {
        public FTest(Dictionary<string, object> testXml)
        {
            details = testXml;
            supportedApps = new List<SupportedApp>();
            if(details.Keys.Contains("supportedApps")) 
                supportedApps.AddRange(details["supportedApps"].ToString().Split(' ').ToList().ConvertAll(x => new SupportedApp() { name = x }));
        }

        public Dictionary<string, object> details { get; set; }

        public string name { get { return details["name"].ToString().Split(':')[1]; } }

        public string featureType { get { return details["name"].ToString().Split(':')[0]; } }

        public List<SupportedApp> supportedApps { get; set; }

        public bool IsSelected { get; set; }

    }
        
    public class CTest
    {
        
        public string name { get { return details["name"].ToString(); } }

        public Dictionary<string,object> details { get; set; }

        public bool IsSelected { get; set; }



    }

    public  class SupportedApp
    {

        public bool IsSelected { get; set; }

        public string name { get; set; }
    }

    public class Test
    {
        public string name { get { return details["name"].ToString(); } }

        public Dictionary<string, object> details { get; set; }

        public bool IsChecked { get; set; }


    }

    public class PlaylistItem : INotifyPropertyChanged
    {


        public string name { get; set; }
        public string appName { get; set; }

        private Status? _status = null;
        public Status? status { get => _status; set { _status = value; OnPropertyChanged(); } }

        private string _output;
        public string output { get => _output; set { _output = value; OnPropertyChanged(); } }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }



    public enum Status
    {
        
        waiting,
        runing,
        PASSED,
        FAILED,
        ERROR


    }


    

    

}
