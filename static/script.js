let weatherData = null;

async function loadWeather() {
  const res = await fetch("/weather");
  weatherData = await res.json();

  // Get today's date string in same format as backend (e.g., "Aug 01")
  const today = new Date();
  const todayStr = today.toLocaleString("en-US", { month: "short", day: "2-digit" });

  // Filter hourly to only today's date
  const todayHourly = weatherData.hourly.filter(h => h.date === todayStr);

  renderHourly(todayHourly, "Today's Hourly Forecast");
  renderDaily(weatherData.daily);
}

function renderHourly(hourly, title) {
  const hourlyDiv = document.getElementById("hourly");
  document.getElementById("day-title").innerText = title;
  hourlyDiv.innerHTML = "";
  hourly.forEach(h => {
    const box = document.createElement("div");
    box.className = "hour-box";
    box.innerHTML = `
      <div><span class="date">${h.date}</span> <span class="time">${h.time}</span></div>
      <h1>${h.emoji}</h1>
      <div>${h.status}</div>
      <div>${h.probability}%</div>
      <div>${h.temperature}°C</div>
    `;
    hourlyDiv.appendChild(box);
  });

  // Auto-scroll to current hour
  const now = new Date();
  const currentHour = now.getHours();
  const scrollTarget = hourlyDiv.children[currentHour];
  if (scrollTarget) {
    scrollTarget.scrollIntoView({behavior: "smooth", inline: "center"});
  }
}

function renderDaily(daily) {
  const dailyDiv = document.getElementById("daily");
  dailyDiv.innerHTML = "";

  const backBtn = document.getElementById("back-btn");
  backBtn.style.display = "none"; // hide initially

  daily.slice(1, 7).forEach(d => {
    const box = document.createElement("div");
    box.className = "day-box";
    box.innerHTML = `
      <div class="date">${d.date}</div>
      <h1>${d.emoji}</h1>
      <div>${d.status}</div>
      <div>Min: ${d.temp_min}°C</div>
      <div>Max: ${d.temp_max}°C</div>
    `;
    box.onclick = () => {
      renderHourly(
        d.hourly.map(h => ({
          date: h.date,
          time: h.time,
          temperature: h.temp,
          status: h.status,
          emoji: h.emoji,
          probability: h.prob
        })),
        `${d.date} Hourly Forecast`
      );
      backBtn.style.display = "inline-block"; // show button when future day selected
    };
    dailyDiv.appendChild(box);
  });

  // Button click restores today's forecast
  backBtn.onclick = () => {
    const today = new Date();
    const todayStr = today.toLocaleString("en-US", { month: "short", day: "2-digit" });
    const todayHourly = weatherData.hourly.filter(h => h.date === todayStr);
    renderHourly(todayHourly, "Today's Hourly Forecast");
    backBtn.style.display = "none"; // hide again
  };
}

loadWeather();

// let weatherData = null;

// async function loadWeather() {
//   const res = await fetch("/weather");
//   weatherData = await res.json();

//   // Show only today's 24 hours initially
//   const today = new Date();
//   const todayStr = today.toLocaleString("en-US", { month: "short", day: "2-digit" });
//   const todayHourly = weatherData.hourly.filter(h => h.date === todayStr);

//   renderHourly(todayHourly, "Today's Hourly Forecast");
//   renderDaily(weatherData.daily);
// }

// function renderHourly(hourly, title) {
//   const hourlyDiv = document.getElementById("hourly");
//   document.getElementById("day-title").innerText = title;
//   hourlyDiv.innerHTML = "";
//   hourly.forEach(h => {
//     const box = document.createElement("div");
//     box.className = "hour-box";
//     box.innerHTML = `
//       <div><span class="date">${h.date}</span> <span class="time">${h.time}</span></div>
//       <h1>${h.emoji}</h1>
//       <div>${h.status}</div>
//       <div>${h.probability}%</div>
//       <div>${h.temperature}°C</div>
//     `;
//     hourlyDiv.appendChild(box);
//   });
// }

// function renderDaily(daily) {
//   const dailyDiv = document.getElementById("daily");
//   dailyDiv.innerHTML = "";

//   const backBtn = document.getElementById("back-btn");
//   backBtn.style.display = "none";

//   daily.slice(1, 7).forEach(d => {
//     const box = document.createElement("div");
//     box.className = "day-box";
//     box.innerHTML = `
//       <div class="date">${d.date}</div>
//       <h1>${d.emoji}</h1>
//       <div>${d.status}</div>
//       <div>Min: ${d.temp_min}°C</div>
//       <div>Max: ${d.temp_max}°C</div>
//     `;
//     box.onclick = () => {
//       renderHourly(d.hourly, `${d.date} Hourly Forecast`);
//       backBtn.style.display = "inline-block";
//     };
//     dailyDiv.appendChild(box);
//   });

//   backBtn.onclick = () => {
//     const today = new Date();
//     const todayStr = today.toLocaleString("en-US", { month: "short", day: "2-digit" });
//     const todayHourly = weatherData.hourly.filter(h => h.date === todayStr);
//     renderHourly(todayHourly, "Today's Hourly Forecast");
//     backBtn.style.display = "none";
//   };
// }

// loadWeather();
