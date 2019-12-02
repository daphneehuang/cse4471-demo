/*
Infosec Project
Teamname:TeamName

Github Scraper


This file will gather necessary usernames and repos
*/

//EDIT THESE
//0, scrape from user
//1, scrape user followers
let operation; //0
let usernameToScrape;// "geerlingguy" //yegor256
let numUsersToScrape; //1000

//program variables
let bigSet2;
let nxurl;
let userCounter;
let unamesToScrape;
let seenUnamesThisRun;
let originalUser;

//dependencies
const gs = require("github-scraper");
const fs = require("fs");




const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})

//get user input
console.log("This program will scrape the followers of a user on github...")
readline.question("--Enter valid github username:", function(name) {
    readline.question("--Enter max number of followers to scrape:", function(maxn) {
        readline.question("--Enter 0 to scrape followers\nOR\n--Enter 1 to scrape the followers of followers\n(data for the user must exist first):", function(opn) {
            usernameToScrape = name
            operation = Number(opn)
            numUsersToScrape = Number(maxn)
            if(operation === NaN || (operation !== 1 && operation !== 0) ){
                operation = 0
            }
            if(numUsersToScrape === NaN){
                numUsersToScrape = 1000
            }

            console.log(`Scraping up to ${numUsersToScrape} followers of ${usernameToScrape} Operation:${operation}`);
            readline.close();
        });
    });
});

//main control
readline.on("close", function() {
    //Main Code
    bigSet2 = new Set();
    nxurl = usernameToScrape+"/followers";
    userCounter = 0;
    unamesToScrape = [];
    seenUnamesThisRun = new Set()
    originalUser = usernameToScrape

    if(operation === 0){
        intervalGet();
    }else if(operation === 1){
        getFollowersOfFollowers();
    }
});







//gets and writes data for a single page of followers
const getOnePage = url => {
    if(url == undefined){
        return;
    }
    gs(url, (err, data) => {
        let pageUsernames = new Set();
        if (data) {
            //console.log("data recieved");
            data.entries.forEach(userdata => {
                bigSet2.add(userdata.username);
                pageUsernames.add(userdata.username);
                userCounter += 1;

                fs.appendFile("./username_data/users_"+numUsersToScrape+"_"+usernameToScrape+"Followers.txt", userdata.username + "\n", err => {
                    // In case of a error throw err.
                    if (err) throw err;
                });
            });
            nxurl = data.next_page;
        }

        if(err){
            nxurl = undefined
            console.log("ERROR!")
            console.log(err)
        }
        
    });
    
};


const hasUserBeenScraped = username =>{
    let res = false
    if(!seenUnamesThisRun.has(username))
    {
        fs.readdirSync("./username_data/").forEach(file => {
         if(file.includes(username)){
                console.log('Data for ' + username + " already exists")
                res = file;
            }
        });
    }
   
     
    return res;
}


const getFollowersOfFollowers = () =>{
    let user = hasUserBeenScraped(usernameToScrape)

    if(user === false){
        console.log("Could not find user")
        process.exit(1)
    }

    console.log("reading " + "./username_data/"+user)
    let lines = fs.readFileSync("./username_data/"+user, 'utf-8')
    .split('\n')
    .filter(Boolean);

    unamesToScrape = lines;
    intervalGet();
}
//makes a request every 10 seconds
const intervalGet = () => {
    let clInterval = false;
    let unameIndex = 0
    if(operation == 1){
        usernameToScrape = unamesToScrape[unameIndex]
        nxurl =  usernameToScrape+"/followers";
    }


    if(hasUserBeenScraped(usernameToScrape) !== false && (operation == 0 || operation === 1 && unamesToScrape.length <= unameIndex) ){
        console.log("Data already exists, please remove data file and scrape again..exiting")
        process.exit(1)
    }else{
        seenUnamesThisRun.add(usernameToScrape)
        console.log("Starting to scrape " + usernameToScrape + " " + nxurl)
        let inter = setInterval(() => {

            if (hasUserBeenScraped(usernameToScrape) !== false || userCounter > numUsersToScrape  || nxurl === undefined ) {
                seenUnamesThisRun.add(usernameToScrape)

                console.log("\tEnded scrape " + usernameToScrape);
                //console.log(seenUnamesThisRun)
                clInterval= true;
                userCounter = 0;

                if( operation === 1 && unameIndex < unamesToScrape.length ){
                    unameIndex++;
                    usernameToScrape = unamesToScrape[unameIndex];
                    nxurl = usernameToScrape+"/followers"
                    console.log("Now scraping from " + usernameToScrape + " " + unameIndex + "/" + unamesToScrape.length)
                }else{
                    clearInterval(inter)
                }
            } else {
                console.log("\tScraping... Recieved:" + userCounter + " URL:" + nxurl);
                getOnePage(nxurl);
            }

           

    }, 10000);
    }
   
   
};













//Legacy Scraping Code
const getNextPage = async url => {
    new Promise((resolve, reject) => {
        console.log("got url " + url);
        gs(url, (err, data) => {
            let pageUsernames = new Set();

            if (data) {
                data.entries.forEach(userdata => {
                    pageUsernames.add(userdata.username);
                });
                console.log(
                    "found " +
                        pageUsernames.size +
                        " on this page url:" +
                        data.next_page
                );
                //console.log(data)

                resolve({
                    nextPageUrl: data.next_page,
                    pageUsernames: pageUsernames
                });
            } else {
                reject();
            }
        });
    });
};

let bigSet = new Set();
const recursiveGet = async (url, numberLeft) => {
    if (numberLeft > 0) {
        getNextPage(url).then(data => {
            console.log("found usernames " + data);
            if (data) {
                console.log(data.pageUsernames);
                bigSet.add(data.pageUsernames);
                getNextPage(data.nextPageUrl, numberLeft - 51);
            }
        });
    }
};

//recursiveGet("fabpot/followers", 2);

const getFollowers = async (user, numberOfUsernames) => {
    //defines number of usernames per person to scrape
    let allUsernames = new Set();

    let nextPageUrl = user + "/followers";
    let usercount = 0;
    let pageCounter = 0;
    console.log("before while");
    while (nextPageUrl && usercount < numberOfUsernames) {
        console.log("in while");

        data2 = await getNextPage(nextPageUrl);
        console.log(data2);
        // pageData = await gs(nextPageUrl, async (err, data) => {
        //     data.entries.forEach(userdata => {
        //         allUsernames.add(userdata.username);
        //     });
        //     nextPageUrl = data.next_page;
        //     pageCounter += 1;
        //     console.log("finished page " + nextPageUrl);
        // });

        if (allUsernames.length > 2) {
            return allUsernames;
        }
        break;
    }
    console.log("after while");
};

//getFollowers("fabpot", 200);
