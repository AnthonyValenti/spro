document.addEventListener('DOMContentLoaded', function() {
    //document.querySelector('#butt').addEventListener('click', () => arbs());
    arbs();


    //the following bunch of code gives the grey background when you hover over an item
    let existingElement1 = document.getElementById("home");
    existingElement1.addEventListener("mouseover", function() {
        addHoverEffect(existingElement1);
    });
    existingElement1.addEventListener("mouseout", function() {
        removeHoverEffect(existingElement1);
    });

    let existingElement2 = document.getElementById("pricing");
    existingElement2.addEventListener("mouseover", function() {
        addHoverEffect(existingElement2);
    });
    existingElement2.addEventListener("mouseout", function() {
        removeHoverEffect(existingElement2);
    });

    let existingElement3 = document.getElementById("arbitrage");
    existingElement3.addEventListener("mouseover", function() {
        addHoverEffect(existingElement3);
    });
    existingElement3.addEventListener("mouseout", function() {
        removeHoverEffect(existingElement3);
    });



    

  });





  function calcClicked(item)
  {
    const calculatorButtons = document.querySelectorAll('.calculator');
    document.querySelector('#calc-clicked').style.display='block';

    


    //when in popup, cannot click other buttons
    calculatorButtons.forEach(button => {
      button.disabled = true;
    });

    console.log(item.game)
    
    //programming the button to close the popup
    const close = document.createElement('button');

    //title of the game and market
    const title = document.createElement('div');

    //the main content within the popup
    const gameInfo = document.createElement('div'); //will be the master div within the popup, close button is outside this

    //will be the div we make the calculations in, child of gameInfo
    const calc = document.createElement('div'); //middle portion of our calc popup, where the books stakes and payouts are shown
    const total_return = document.createElement('div'); //bottom portion of calculator pop up
    const total_stake = document.createElement('div'); //total stake div
    const total_payout = document.createElement('div'); //total payout div
    const profit = document.createElement('div'); //profit div
    const headings = document.createElement('div'); //for our stake and payout headings
    const titles = document.createElement('div'); //for our title of team name odds and book
    


    const stake1 = document.createElement('input');
    const stake2 = document.createElement('input');

    const payout1 = document.createElement('input');
    const payout2 = document.createElement('input');

    stake1.type = 'number';
    stake2.type = 'number';
    stake1.placeholder = '100'
    stake2.placeholder = '100'
    stake1.setAttribute('max', '2'); // Use setAttribute to set max
    stake2.setAttribute('max', '2'); // Use setAttribute to set max

    stake1.classList.add('stake1')
    stake2.classList.add('stake2')

    payout1.classList.add('payout1')
    payout2.classList.add('payout2')
    payout1.disabled = true;
    payout2.disabled = true;
    payout1.placeholder = '0.00'
    payout2.placeholder = '0.00'
    
    
    total_return.classList.add('total-return')
    title.classList.add('popup-title')
    gameInfo.classList.add('game-info')
    calc.classList.add('popup-calc')
    total_payout.classList.add('total-payout')
    total_stake.classList.add('total-stake')
    headings.classList.add('headings')
    titles.classList.add('titles')

    profit.classList.add('profit')

    total_stake.innerHTML = `Total Stake <br> --`
    total_payout.innerHTML = `Total Payout <br> --`
    profit.innerHTML = `Profit (--%) <br> --`

    stake1.addEventListener('input', function(e){
      let val1 = e.target.value

      // Check if the value is an integer using a regular expression
      if (/^\d+$/.test(val1)) {
        console.log('Valid integer:', val1);

        if (val1 > 100000) 
        {
          // If it is, set the value to 100000
          e.target.value = 100000;
          val1=100000;
        }
        //pass to function to get stake 2 value
        let result = calculation(item.team1[0].odds,item.team2[0].odds,val1)

        let wager = result[0];
        let total1 = result[1];
        let total2 = result[2];

        console.log(wager, total1, total2)

        stake2.value = wager;
        payout1.value = (Math.round(total1 * 100) / 100).toFixed(2);
        payout2.value = (Math.round(total2 * 100) / 100).toFixed(2);

        let stakey = parseInt(val1)+parseFloat(wager.toFixed(2))
        let totalStake = ((Math.round(stakey * 100) / 100).toFixed(2))
        let totalPayout = parseFloat(total1.toFixed(2))
        let totalProfit = parseFloat((totalPayout - totalStake).toFixed(2))
        let totalProfitPercent = parseFloat(((totalProfit/totalPayout)*100).toFixed(2))


        total_stake.innerHTML = `Total Stake <br> <span id='num-format'>$${totalStake}</span>`
        total_payout.innerHTML = `Total Payout <br> <span id='num-format'>$${(Math.round(totalPayout * 100) / 100).toFixed(2)}</span>`
        profit.innerHTML = `Profit (${totalProfitPercent}%) <br> <span id='num-format'>$${(Math.round(totalProfit * 100) / 100).toFixed(2)}</span>`

      } else {
        console.log('Not a valid integer');
        stake2.value='';
        payout1.value='';
        payout2.value='';
        total_stake.innerHTML = `Total Stake <br> --`
        total_payout.innerHTML = `Total Payout <br> --`
        profit.innerHTML = `Profit (--%) <br> --`
      }

    });


    stake2.addEventListener('input', function(e){
      let val2 = e.target.value

      // Check if the value is an integer using a regular expression
      if (/^\d+$/.test(val2)) {
        console.log('Valid integer:', val2);

        if (val2 > 100000) 
        {
          // If it is, set the value to 100000
          e.target.value = 100000;
          val2=100000;
        }


        //pass to function to get stake 2 value
        let result = calculation(item.team2[0].odds,item.team1[0].odds,val2)

        let wager = result[0];
        let total1 = result[1];
        let total2 = result[2];

        console.log(wager, total1, total2)

        stake1.value = (Math.round(wager * 100) / 100).toFixed(2);
        payout1.value = (Math.round(total1 * 100) / 100).toFixed(2);
        payout2.value = (Math.round(total2 * 100) / 100).toFixed(2);

        let stakey = parseInt(val2)+parseFloat(wager.toFixed(2))
        let totalStake = ((Math.round(stakey * 100) / 100).toFixed(2))
        let totalPayout = parseFloat(total1.toFixed(2))
        let totalProfit = parseFloat((totalPayout - totalStake).toFixed(2))
        let totalProfitPercent = parseFloat(((totalProfit/totalPayout)*100).toFixed(2))

        total_stake.innerHTML = `Total Stake <br> <span id='num-format'>$${totalStake}</span>`
        total_payout.innerHTML = `Total Payout <br> <span id='num-format'>$${(Math.round(totalPayout * 100) / 100).toFixed(2)}</span>`
        profit.innerHTML = `Profit (${totalProfitPercent}%) <br> <span id='num-format'>$${(Math.round(totalProfit * 100) / 100).toFixed(2)}</span>`

      } else {
        console.log('Not a valid integer');
        //give alert below box that it needs to be an int
        stake1.value='';
        payout1.value='';
        payout2.value='';
        total_stake.innerHTML = `Total Stake <br> --`
        total_payout.innerHTML = `Total Payout <br> --`
        profit.innerHTML = `Profit (--%) <br> --`
      }
    });

    
    if (item.market == 'Moneyline')
    {
      title.innerHTML = `${item.game}<br><span id='popup-market'>${item.market}</span>`
    }
  

    close.innerHTML = `<button type="button" class="btn-close btn-close-white" aria-label="Close"></button>`


    close.addEventListener('click', function(){
      document.querySelector('#calc-clicked').style.display='none';
      document.querySelector('#calc-clicked').innerHTML = '';
      calculatorButtons.forEach(button => {
        button.disabled = false;
      });
      
    });

    titles.innerHTML = `<span id='popup-team1'>${item.team1[0].name} <br>${item.team1[0].odds} <a href=${item.team1[0].link} target="_blank" style="text-decoration: none; font-weight: bold; color: white;">${item.team1[0].book}</a></span> 
                          <span id='popup-team2'>${item.team2[0].name} <br>${item.team2[0].odds} <a href=${item.team2[0].link} target="_blank" style="text-decoration: none; font-weight: bold; color: white;">${item.team2[0].book}</a></span>`


    calc.innerHTML = `<br>Stake<br><br><br>Payout`

    
    
    total_return.appendChild(total_stake)
    total_return.appendChild(total_payout)
    total_return.appendChild(profit)
    
    calc.appendChild(stake1)
    calc.appendChild(stake2)
    calc.appendChild(payout1)
    calc.appendChild(payout2)
   
    gameInfo.appendChild(titles)
    gameInfo.appendChild(calc)
    gameInfo.appendChild(total_return)
   

    
    document.querySelector('#calc-clicked').appendChild(close)
    document.querySelector('#calc-clicked').appendChild(gameInfo)
    document.querySelector('#calc-clicked').appendChild(title)

  }





  function addHoverEffect(existingElement) 
  {
    existingElement.classList.add("hover-background");
  }

  function removeHoverEffect(existingElement) 
  {
    existingElement.classList.remove("hover-background");
  }





  function arbs()
  {
    
    console.log('hello')

    // fetch('http://127.0.0.1:8000')
    fetch('http://127.0.0.1:5500/test-spro/index.html')
    .then(response => response.text())
    .then(contents => {
        //console.log(contents)

        // const dataObject = JSON.parse(contents);

      
        // const nhlArray = dataObject.NHL;
        // const nbaArray = dataObject.NBA;
        // const nflArray = dataObject.NFL;


        //i made this change just to make editing the webpage easier. when you want the real thing, fix the fetch url to the real thing, remove everything between the slashes, and uncomment above
        
        //////////////////////////////////////////////
        let x =   {"NHL":[],"NBA":[{"sport":"NBA","time":"8:58 PM EST","game":"Chicago Bulls vs Charlotte Hornets","when":"Today","market":"Moneyline","team1":[{"name":"Chicago Bulls","book":"Pointsbet","odds":"-140","link":"https://on.pointsbet.ca/sports/basketball/NBA"}],"team2":[{"name":"Charlotte Hornets","book":"Northstar","odds":"+180","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Oklahoma City Thunder vs Washington Wizards","when":"Today","market":"Moneyline","team1":[{"name":"Oklahoma City Thunder","book":"Pointsbet","odds":"-2500","link":"https://on.pointsbet.ca/sports/basketball/NBA"}],"team2":[{"name":"Washington Wizards","book":"888","odds":"+2800","link":"https://www.888sport.ca/basketball/nba/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Boston Celtics vs Indiana Pacers","when":"Today","market":"Moneyline","team1":[{"name":"Indiana Pacers","book":"Pointsbet","odds":"+110","link":"https://on.pointsbet.ca/sports/basketball/NBA"}],"team2":[{"name":"Boston Celtics","book":"Northstar","odds":"+114","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Houston Rockets","book":"Pointsbet","odds":"+250","link":"https://on.pointsbet.ca/sports/basketball/NBA"}],"team2":[{"name":"Miami Heat","book":"Betano","odds":"-167","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Utah Jazz vs Milwaukee Bucks","when":"Today","market":"Moneyline","team1":[{"name":"Utah Jazz","book":"Pointsbet","odds":"-1000","link":"https://on.pointsbet.ca/sports/basketball/NBA"}],"team2":[{"name":"Milwaukee Bucks","book":"Northstar","odds":"+1300","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Houston Rockets","book":"Betrivers","odds":"+285","link":"https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches"}],"team2":[{"name":"Miami Heat","book":"Draftkings","odds":"-280","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Houston Rockets","book":"Betrivers","odds":"+285","link":"https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches"}],"team2":[{"name":"Miami Heat","book":"Betano","odds":"-167","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Boston Celtics vs Indiana Pacers","when":"Today","market":"Moneyline","team1":[{"name":"Indiana Pacers","book":"Draftkings","odds":"-110","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}],"team2":[{"name":"Boston Celtics","book":"Northstar","odds":"+114","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Chicago Bulls vs Charlotte Hornets","when":"Today","market":"Moneyline","team1":[{"name":"Chicago Bulls","book":"Draftkings","odds":"-175","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}],"team2":[{"name":"Charlotte Hornets","book":"Northstar","odds":"+180","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Houston Rockets","book":"Draftkings","odds":"+210","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}],"team2":[{"name":"Miami Heat","book":"Betano","odds":"-167","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Miami Heat","book":"Draftkings","odds":"-280","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}],"team2":[{"name":"Houston Rockets","book":"Score","odds":"+305","link":"https://thescore.bet/sport/basketball/organization/united-states/competition/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Utah Jazz vs Milwaukee Bucks","when":"Today","market":"Moneyline","team1":[{"name":"Utah Jazz","book":"Draftkings","odds":"-1050","link":"https://sportsbook.draftkings.com/leagues/basketball/nba"}],"team2":[{"name":"Milwaukee Bucks","book":"Northstar","odds":"+1300","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Boston Celtics vs Indiana Pacers","when":"Today","market":"Moneyline","team1":[{"name":"Boston Celtics","book":"Northstar","odds":"+114","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}],"team2":[{"name":"Indiana Pacers","book":"Betano","odds":"-110","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Boston Celtics vs Indiana Pacers","when":"Today","market":"Moneyline","team1":[{"name":"Boston Celtics","book":"Northstar","odds":"+114","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}],"team2":[{"name":"Indiana Pacers","book":"Score","odds":"+105","link":"https://thescore.bet/sport/basketball/organization/united-states/competition/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Chicago Bulls vs Charlotte Hornets","when":"Today","market":"Moneyline","team1":[{"name":"Charlotte Hornets","book":"Northstar","odds":"+180","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}],"team2":[{"name":"Chicago Bulls","book":"Score","odds":"-165","link":"https://thescore.bet/sport/basketball/organization/united-states/competition/nba"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Houston Rockets","book":"Northstar","odds":"+275","link":"https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba"}],"team2":[{"name":"Miami Heat","book":"Betano","odds":"-167","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}]},{"sport":"NBA","time":"8:58 PM EST","game":"Houston Rockets vs Miami Heat","when":"Today","market":"Moneyline","team1":[{"name":"Miami Heat","book":"Betano","odds":"-167","link":"https://www.betano.ca/sport/basketball/north-america/nba/441g/"}],"team2":[{"name":"Houston Rockets","book":"Score","odds":"+305","link":"https://thescore.bet/sport/basketball/organization/united-states/competition/nba"}]}],"NFL":[]}
        nhlArray = x.NHL
        nbaArray = x.NBA
        nflArray = x.NFL
        //////////////////////////////////////////////
        

        console.log(nhlArray)
        console.log(nbaArray)
        console.log(nflArray)

        // Concatenate all arrays into a single array
        const allData = [nhlArray, nbaArray, nflArray];

        // Check if any of the arrays has entries
        const anyArrayHasEntries = nhlArray.length > 0 || nbaArray.length > 0 || nflArray.length > 0;

        // Call populateTable only if there are entries
        if (anyArrayHasEntries) 
        {
          // Concatenate all arrays into a single array
          const allData = [...nhlArray, ...nbaArray, ...nflArray];

          // Call populateTable with the combined data
          populateTable(allData);
          
      }
      else
      {
        // Show/hide the "No bets" message based on whether there are entries
        document.querySelector('#no-bets-message').style.display='block';
      }

    })//then contents close

  } //arbs function close





  function populateTable(data) 
  {
    
    document.querySelector('#no-bets-message').style.display='none';
    const tableBody = document.getElementById("dynamic-table-all").getElementsByTagName('tbody')[0];

    // Clear existing rows
    tableBody.innerHTML = ''; //will fix later to keep the entries still in the list and remove those which arent anymore, currently itll clear everything which isnt ideal, but for now will suffice

    // Loop through the data and create rows
    data.forEach(item => { //item repersents each idnivudal arb bet
        const row = tableBody.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        const cell3 = row.insertCell(2);
        const cell4 = row.insertCell(3);
        const cell5 = row.insertCell(4);
        const cell6 = row.insertCell(5);
        const cell7 = row.insertCell(6);
        const cell8 = row.insertCell(7);

        //cell1.textContent = item.percent; will need to be calculated (probably via a function)
        cell1.innerHTML =   `<button class='calculator'><img class='calculator' src="./images/calculator (2).png" alt="calculator button"></img></button>`
        
        // Assign the event listener to each calculator button
        const calculatorButton = cell1.querySelector('button');
        calculatorButton.addEventListener('click', function () {
          calcClicked(item); // Assuming calcClicked function takes an argument
        });

        cell2.innerHTML = `${getPercent(item.team1[0].odds, item.team2[0].odds)}%` //double check this, needs to be reviewed
        cell3.innerHTML = item.when //today
        cell4.innerHTML = `<b>${item.game}</b><br>${item.sport}`; //leafs vs mtl, NHL
        cell5.textContent = item.market; //moneyline
        cell8.innerHTML = item.time; //last updated

        
        if (item.market == 'Moneyline')
        {
          cell6.innerHTML = `<span id='bets'>${item.team1[0].name}<br>${item.team2[0].name}</span>`
          cell7.innerHTML = `<span id='books'>${item.team1[0].odds} <a href=${item.team1[0].link} target="_blank" style="text-decoration: none; font-weight: 900; color: white;">${item.team1[0].book}</a><br>${item.team2[0].odds} <a href=${item.team2[0].link} target="_blank" style="text-decoration: none; font-weight: 900; color: white;">${item.team2[0].book}</a></span>`
        }

        else if (item.market == 'Total' || item.market == 'Spread')
        {
          //cell6.innerHTML = `${item.team1[0].count} &nbsp ${item.team1[0].odds} on <a href=${item.team1[0].link} target="_blank" style="text-decoration: none; font-weight: bold; color: white;">${item.team1[0].book}</a> <br> ${item.team2[0].count} &nbsp ${item.team2[0].odds} on <a href=${item.team2[0].link} target="_blank" style="text-decoration: none; font-weight: bold; color: white;">${item.team2[0].book}</a>`
          cell6.innerHTML = `<span id='bets'>${item.team1[0].name} ${item.team1[0].count}<br>${item.team2[0].name} ${item.team2[0].count}</span>`
          cell7.innerHTML = ` <span id='books'>${item.team1[0].odds} <a href=${item.team1[0].link} target="_blank" style="text-decoration: none; font-weight: 900; color: white;">${item.team1[0].book}</a><br>${item.team2[0].odds} <a href=${item.team2[0].link} target="_blank" style="text-decoration: none; font-weight: 900; color: white;">${item.team2[0].book}</a></span>`
        }

    });
  }


  

  function getPercent(odds1, odds2)
  {

    let wager1 = 1000;
    let total1, total2, ratio, wager2, return1, return2;

    if (String(odds1)[0] === '-') 
    {
        total1 = 1 + 100 / Math.abs(odds1);
    } 
    else 
    {
      total1 = 1 + odds1 / 100;
    }

    if (String(odds2)[0] === '-') 
    {
      total2 = 1 + 100 / Math.abs(odds2);
    } 
    else 
    {
      total2 = 1 + odds2 / 100;
    }

    ratio = total2 / total1;
    wager2 = wager1 / ratio;

    if (String(odds1)[0] === '-') 
    {
      payout1 = (1+(100 / Math.abs(odds1))) * wager1;
    } 
    else 
    {
      payout1 = (1+(odds1 / 100)) * wager1;
    }

    if (String(odds2)[0] === '-') 
    {
      payout2 = (1+(100 / Math.abs(odds2))) * wager2;
    } 
    else 
    {
      payout2 = (1+(odds2 / 100)) * wager2;
    }

    let totalStake = parseFloat(wager1.toFixed(2))+parseFloat(wager2.toFixed(2))
    let totalPayout = parseFloat(payout1.toFixed(2))
    let totalProfit = parseFloat((totalPayout - totalStake).toFixed(2))
    let totalProfitPercent = parseFloat(((totalProfit/totalPayout)*100).toFixed(2))

    
    return (Math.round(totalProfitPercent  * 100) / 100).toFixed(2);
  }





  function calculation(odds1, odds2, wager1)
  {
    let total1, total2, ratio, wager2, return1, return2;

    if (String(odds1)[0] === '-') 
    {
        total1 = 1 + 100 / Math.abs(odds1);
    } 
    else 
    {
      total1 = 1 + odds1 / 100;
    }

    if (String(odds2)[0] === '-') 
    {
      total2 = 1 + 100 / Math.abs(odds2);
    } 
    else 
    {
      total2 = 1 + odds2 / 100;
    }

    ratio = total2 / total1;
    wager2 = wager1 / ratio;

    if (String(odds1)[0] === '-') 
    {
      payout1 = (1+(100 / Math.abs(odds1))) * wager1;
    } 
    else 
    {
      payout1 = (1+(odds1 / 100)) * wager1;
    }

    if (String(odds2)[0] === '-') 
    {
      payout2 = (1+(100 / Math.abs(odds2))) * wager2;
    } 
    else 
    {
      payout2 = (1+(odds2 / 100)) * wager2;
    }
    
    return [parseFloat(wager2.toFixed(2)), parseFloat(payout1.toFixed(2)), parseFloat(payout2.toFixed(2))]
  }




// arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Moneyline', 
//                   'team1':[{'name':team12, 'book':book1, 'odds':moneyline12}],
//                   'team2':[{'name':team21, 'book':book2, 'odds':moneyline21}]})


// arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Total', 
// 'team1':[{'name':team12, 'book':book1, 'count':total_count12, 'odds':total_odds12}],
// 'team2':[{'name':team21, 'book':book2, 'count':total_count21, 'odds':total_odds21}]})



//to do:
//fix mgm whys it not processing for nhl and nfl
//change book name to its logo?
//fix table alignment, feel like its variabkle where if a long team name comes along itll get messed up, need it to be more consistent in width and stuff, maybe it is? idk need to test
//the score nfl not working, draftkings nfl not working


//read here
//1) Ensure consistent alignment across different window sizes
//2) fix backend stuff, see above i.e mgm not working for nhl nfl, score & dk nfl not working, etc
//want to deploy backend, get that working and make sure it works is important

//tomorrow we deploy no more messing around then fix backend stuff