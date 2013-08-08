$(document).ready(function(){
	getHistory();
	$("#txtPaymentDate").datetimepicker();
});

var formatDate = function(unformatted) {
	var dateObj = new Date(unformatted);
	return ("0" + (dateObj.getMonth() + 1)).slice(-2) + " - " + 
		("0" + dateObj.getDate()).slice(-2) + " - " + 
		dateObj.getFullYear();
};

var getHistory = function() {
	$.get("/BillMinder/" + BillMinder.billID + "/history/", function(data) {
		drawGraph(data);
		drawTable(data);
	});
};

var drawGraph = function(data) {
	var chartContext;
	var chartData = {
		labels: [],
		datasets: [{
			fillColor : "rgba(0, 158, 0, 0.5)",
			strokeColor : "rgba(64, 255, 128, 0.5)",
			pointColor : "rgba(0, 64, 0, 0.8)",
			pointStrokeColor : "#fff",
			data: []
		}]
	};
	var billChart;
	if(data.length > 1) {
		for(var x = 0; x < data.length; x++) {
			chartData.labels.push(formatDate(data[x].fields.payment_date));
			chartData.datasets[0].data.push(+data[x].fields.payment_amount);
		}
		chartContext = document.getElementById("billChart").getContext("2d");
		billChart = new Chart(chartContext).Line(chartData);
	}
};

var drawTable = function(data) {
	// TODO: create or apply table creation tool
	var container = document.getElementById("divRecentPayments");
	container.innerHTML = "";
	var tbl = document.createElement("table");
	var thead = document.createElement("thead");
	var trHead = document.createElement("tr");
	var thDate = document.createElement("th");
	thDate.innerHTML = "Payment Date";
	trHead.appendChild(thDate);
	var thAmount = document.createElement("th");
	thAmount.innerHTML = "Payment Amount";
	trHead.appendChild(thAmount);
	var thNotes = document.createElement("th");
	thNotes.innerHTML = "Notes";
	trHead.appendChild(thNotes);
	thead.appendChild(trHead);
	tbl.appendChild(thead);
	var tbody = document.createElement("tbody");
	var recordCount = data.length;
	var tr;
	var tdDate;
	var tdAmount;
	var tdNotes;
	for(var i = 0; i < recordCount; i++) {
		tr = document.createElement("tr");
		tdDate = document.createElement("td");
		tdDate.innerHTML = formatDate(data[i].fields.payment_date);
		tr.appendChild(tdDate);
		tdAmount = document.createElement("td");
		tdAmount.innerHTML = "$" + data[i].fields.payment_amount;
		tr.appendChild(tdAmount);
		tdNotes = document.createElement("td");
		tdNotes.innerHTML = data[i].fields.notes;
		tr.appendChild(tdNotes);
		tbody.appendChild(tr);
	}
	tbl.appendChild(tbody);
	container.appendChild(tbl);						
};

var showPayment = function() {
	var now = new Date();
	document.getElementById("txtPaymentDate").value = ("0" + (now.getMonth() + 1)).slice(-2) + "/" +
		("0" + now.getDate()).slice(-2) + "/" + now.getFullYear() + " " + 
		("0" + now.getHours()).slice(-2) + ":" + ("0" + now.getMinutes()).slice(-2); 
	$('#divAddEntry').show(100, function() {
		document.getElementById("txtPaymentAmount").select();
		document.getElementById("txtPaymentAmount").focus();
	});
};

var makePayment = function() {
	$.post("/BillMinder/" + BillMinder.billID + "/pay/", {
		payment_date: document.getElementById("txtPaymentDate").value,
		amount: document.getElementById("txtPaymentAmount").value,
		reminder_days: document.getElementById("txtReminderDays").value,
		confirmation_number: document.getElementById("txtConfirmationNumber").value,
		notes: document.getElementById("txtNotes").value
	},
    function(data) {
		$('#divAddEntry').hide(250, function() {
			document.getElementById("txtConfirmationNumber").value = "";
			document.getElementById("txtNotes").value = "";					
		});
		drawGraph();
	}).error(function(jqXHR, status, error) { alert(error); });
};