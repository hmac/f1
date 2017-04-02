// ----- Setup ----- //

const DRIVER_TOTAL = 1000;
const TEAM_TOTAL = 1000;


// ----- Functions ----- //

// Retrieves the drivers and teams from the page.
function getElems () {

    return {
	drivers: document.querySelectorAll('.driver-table input[type=checkbox]:checked'),
	teams: document.querySelectorAll('.team-table input[type=checkbox]:checked')
    };
    
}

// Sums a list of objects with a price field.
function sumPrices (total, {price}) {
    return total + parseInt(price);
}

// Calculates whether the spend is within budget.
function withinBudget (drivers, teams) {

    let driverTotal = drivers.reduce(sumPrices, 0);
    let teamTotal = teams.reduce(sumPrices, 0);
    console.log(driverTotal, teamTotal);

    return (teamTotal <= TEAM_TOTAL) && (driverTotal <= DRIVER_TOTAL);
    
}

// Retrieves the drivers and teams bought, and checks the total is within budget.
function getPurchase (elems) {

    let drivers = Array.from(elems.drivers, driver => {
	return { name: driver.dataset.driver, price: driver.dataset.price };
    });

    let teams = Array.from(elems.teams, team => {
	return { name: team.dataset.team, price: team.dataset.price };
    });

    if (withinBudget(drivers, teams)) {
	alert('yay!');
    } else {
	alert('you spent too much!');
    }

}


// ----- Run ----- //

document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('purchase').addEventListener('click', () => {
	getPurchase(getElems());
    });

});
