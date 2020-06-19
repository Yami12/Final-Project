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

namespace try_python_connection
{
    public class Data 
    {
        public Data()
        {

            
            cTests = new ObservableCollection<CTest>(loadCtestsFromXML());
            fTests = new ObservableCollection<FTest>(loadFtestsFromXML());
            loadAppsFromXML();
            //messagingSocialNetworks = new ObservableCollection<MessagingSocialNetwork>(loadMessagingSocialNetworksFromXML());
            //rfgSocialNetworks = new ObservableCollection<RfgSocialNetwork>(loadRfgSocialNetworksFromXML());
            //fTestsPlaylist= new ObservableCollection<FTest>();
            //foreach (var ft in fTests)
            //    if (ft.name == "Removal from group")
            //        ft.socialNetworks = new List<SocialNetwork>(rfgSocialNetworks);
            //    else
            //        ft.socialNetworks = new List<SocialNetwork>(messagingSocialNetworks.ToList().ConvertAll(x => new MessagingSocialNetwork(x)));
               
        }

        private void Data_playlistChange(bool isFtest, object test, bool isAdd)
        {



            //if (isFtest)
            //{
            //    if (fTestsPlaylist.Contains((FTest)test))
            //        fTestsPlaylist.Remove((FTest)test);
            //    else
            //        fTestsPlaylist.Add((FTest)test);
            //}
            //else
            //{
            //    if (cTestsPlaylist.Contains((CTest)test))
            //        cTestsPlaylist.Remove((CTest)test);
            //    else
            //        cTestsPlaylist.Add((CTest)test);
            //}

        }

        public void UpdatePlaylist(FTest fTest)
        {
            if (fTest.supportedApps.Count == 0) //test without supported apps
                if (fPlaylist.Any(x => x.name == fTest.name)) fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name)); else fPlaylist.Add(new FPlTest() { name = fTest.name });
            foreach (var app in fTest.supportedApps)
            {
                if (fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name)  && !app.IsSelected)
                    fPlaylist.Remove(fPlaylist.First(x => x.name == fTest.name && x.appName == app.name));
                else if (!fPlaylist.Any(x => x.name == fTest.name && x.appName == app.name) && app.IsSelected)
                    fPlaylist.Add(new FPlTest() { name = fTest.name, appName = app.name });


            }
            //if (fPlaylist.Any(x=> x.name == testName && x.appsName == appsName))
            //    fPlaylist.Remove(fPlaylist.First(x => x.name == testName && x.appssName == appsName));
            //else
            //    fPlaylist.Add(new FPlTest() { name = testName , appName = appsName});

            // fPlaylist.Remove(x => true);

            // foreach(var ft in fTestsPlaylist)
            // {
            //     foreach(var sn in ft.socialNetworks)
            //     {
            //         if(sn.IsSelected)
            //             fPlaylist.Add(new FPlTest() { name = ft.name, SocialNetworkName = sn.name });
            //     }
            // }
            //;
        }



        public ObservableCollection<FTest> fTests { get; set; }

        public HashSet<string> featuresList { get { return fTests.ToList().ConvertAll(x => x.test["name"].Split(':')[0]).ToHashSet(); } }
        public ICollectionView featureTests { get { return CollectionViewSource.GetDefaultView(fTests); } }


        public ObservableCollection<CTest> cTests { get; set; }

        public ObservableCollection<FPlTest> fPlaylist { get; set; }

        public ObservableCollection<PlTest> cPlaylist { get; set; }




        public int currentTest { get; set; }

        public List<string> Devices { get; set; }




        public List<CTest> loadCtestsFromXML()
        {
            XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\components_behavior_tests.xml");

            var lv1s = from lv1 in xdoc.Descendants("test")
                       select new CTest()
                       {
                           name = lv1.Element("name").Value,
                           expectedResult = lv1.Element("expectedResult").Value,
                           steps = lv1.Descendants("steps").Descendants("step").ToList().Select(y => y.Descendants().ToDictionary(x => x.Name.LocalName, x => (string)x.Value)).ToList()
                        };
            return lv1s.ToList();

        }

        public List<FTest> loadFtestsFromXML()
        {
            XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\feature_tests.xml");

            var ldict = from lv1 in xdoc.Descendants("test")
                        select new FTest(lv1.Descendants().ToDictionary(x => x.Name.LocalName, x => (string)x.Value));
                        

            return ldict.ToList();

        }

        public List<Dictionary<string, object>> loadAppsFromXML()
        {
            
            XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\apps.xml");
            var appsList = new List<Dictionary<string, object>>();
            foreach(var des in xdoc.Descendants("app").Elements())
            {
                var app = new Dictionary<string, object>();
                if (des.HasElements)
                    app.Add(des.Name.LocalName, new List<Dictionary<string, object>>().Append(des.Descendants(des.Name.LocalName).Descendants().ToDictionary(x => x.Name.LocalName, x => (object)x.Value)));
                else
                    app.Add(des.Name.LocalName, des.Value);
            }
            return appsList;
                       
        }

        public List<MessagingSocialNetwork> loadMessagingSocialNetworksFromXML()
        {
            XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\social_networks.xml");

            var ldict = from lv1 in xdoc.Descendants("social_network")
                        select new MessagingSocialNetwork()
                        {
                            name = lv1.Element("name").Value,
                            app_package = lv1.Element("app_package").Value,
                            app_activity = lv1.Element("app_activity").Value,
                            parent_name = lv1.Element("parent_name").Value,
                            child_name = lv1.Element("child_name").Value,
                            steps = lv1.Descendants("steps").Descendants("step").ToList().Select(y => y.Descendants().ToDictionary(x => x.Name.LocalName, x => (string)x.Value)).ToList()

                        };

            return ldict.ToList();

        }

        public List<RfgSocialNetwork> loadRfgSocialNetworksFromXML()
        {
            XDocument xdoc = XDocument.Load(@"C:\Users\israel\source\repos\try_python_connection\try_python_connection\xml files\removal_from_group.xml");

            var ldict = from lv1 in xdoc.Descendants("social_network")
                        select new RfgSocialNetwork()
                        {
                            name = lv1.Element("name").Value,
                            group_name = lv1.Element("group_name").Value,
                            steps = lv1.Descendants("steps").Descendants("step").ToList().Select(y => y.Descendants().ToDictionary(x => x.Name.LocalName, x => (string)x.Value)).ToList()

                        };

            return ldict.ToList();

        }



    }


    public class FTest
    {
        public FTest(Dictionary<string, string> testXml)
        {
            test = testXml;
            supportedApps = new List<SupportedApp>();
            if(test.Keys.Contains("supportedApps")) 
                supportedApps.AddRange(test["supportedApps"].Split(' ').ToList().ConvertAll(x => new SupportedApp() { name = x }));
        }

        public Dictionary<string, string> test { get; set; }

        public string name { get { return this.test["name"].Split(':')[1]; } }

        public string featureType { get { return test["name"].Split(':')[0]; } }

        public List<SupportedApp> supportedApps { get; set; }

        public bool IsSelected { get; set; }

    }

    
    public class CTest
    {
        
        public string name { get; set; }

        
        public string expectedResult { get; set; }

        
        public List<Dictionary<string, string>> steps { get; set; }

        public bool IsSelected { get; set; }



    }



    public  class SupportedApp
    {

        public bool IsSelected { get; set; }

        //private bool isSelected;
        //public bool IsSelected { get { return isSelected; } set { isSelected = value; Data.RaiseEvent(true,this, value); } }

        public string name { get; set; }
    }

    public class MessagingSocialNetwork : SupportedApp
    {
        public MessagingSocialNetwork(MessagingSocialNetwork msn)
        {
            name = msn.name;
            IsSelected = msn.IsSelected;
            app_package = msn.app_package;
            app_activity = msn.app_activity;
            parent_name = msn.parent_name;
            child_name = msn.child_name;
            steps = msn.steps;

        }

        public MessagingSocialNetwork()
        {

        }

        public string app_package { get; set; }
        public string app_activity { get; set; }
        public string parent_name { get; set; }
        public string child_name { get; set; }
        public List<Dictionary<string, string>> steps { get; set; }
        

    }

    public class RfgSocialNetwork :SupportedApp
    {
        

        public string group_name { get; set; }

        public List<Dictionary<string, string>> steps { get; set; }
    }

    public class PlTest
    {
        public string name { get; set; }

        public Status status { get; set; }

        public bool passed { get; set; }


    }

    public class FPlTest : PlTest
    {
        public string appName { get; set; }
    }

    public enum Status
    {

    }


    public static class ExtensionMethods
    {
        public static int Remove<T>(
            this ObservableCollection<T> coll, Func<T, bool> condition)
        {
            var itemsToRemove = coll.Where(condition).ToList();

            foreach (var itemToRemove in itemsToRemove)
            {
                coll.Remove(itemToRemove);
            }

            return itemsToRemove.Count;
        }
    }

    

}
