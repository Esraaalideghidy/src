function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime) {
  var clock = document.getElementById(id);
  var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);
  
    if (t.total <= 0) {
      daysSpan.innerHTML = '00';
      hoursSpan.innerHTML = '00';
      minutesSpan.innerHTML = '00';
      secondsSpan.innerHTML = '00';
      clearInterval(timeinterval);
      return;
    }
  
    daysSpan.innerHTML = t.days;
    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}

var clockDiv = document.getElementById('clockdiv');

if (clockDiv) {
  var dealEnd = clockDiv.getAttribute('data-deal-end');

  if (dealEnd) {
    var deadline = new Date(Date.parse(dealEnd));
    initializeClock('clockdiv', deadline);
  }
}
