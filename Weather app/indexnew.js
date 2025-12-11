const apiKey = "a8ffbf811dcebb1baf2f102d801aa5f5";
const apiUrl = "https://api.openweathermap.org/data/2.5/weather?units=metric&q=";

const searchBox = document.querySelector(".search input");
const searchBtn = document.querySelector(".search button");
const weatherIcon = document.querySelector(".weather-icon");

async function checkWeather(city) {
  const response = await fetch(apiUrl + city + `&appid=${apiKey}`);

  if (response.status === 404) {
    document.querySelector(".error").style.display = "block";
    document.querySelector(".weather").style.display = "none";
    document.querySelector(".suggestion").innerHTML = "";
  } else {
    const data = await response.json();
    const userMood = document.getElementById("userMood").value;

    document.querySelector(".city").innerHTML = data.name;
    document.querySelector(".temp").innerHTML = Math.round(data.main.temp) + "°C";
    document.querySelector(".humidity").innerHTML = data.main.humidity + "%";
    document.querySelector(".wind").innerHTML = data.wind.speed + " km/h";

    // Set correct icon
    if (data.weather[0].main === "Clouds") {
      weatherIcon.src = "weather-app-img/images/clouds.png";
    } else if (data.weather[0].main === "Rain") {
      weatherIcon.src = "weather-app-img/images/rain.png";
    } else if (data.weather[0].main === "Clear") {
      weatherIcon.src = "weather-app-img/images/clear.png";
    } else if (data.weather[0].main === "Drizzle") {
      weatherIcon.src = "weather-app-img/images/drizzle.png";
    } else if (data.weather[0].main === "Mist") {
      weatherIcon.src = "weather-app-img/images/mist.png";
    }

    // Suggestion logic
    let suggestion = "";
    const weatherType = data.weather[0].main;

    if (weatherType === "Rain") {
      if (userMood === "cozy") {
        suggestion = "Rainy and cozy—perfect for chai, a blanket, and your favorite book.";
      } else if (userMood === "active") {
        suggestion = "Rainy outside, but you could do a home workout or dance session indoors!";
      } else {
        suggestion = "Rainy day? Invite friends over for board games or a movie marathon.";
      }
    } else if (weatherType === "Clear") {
      if (userMood === "cozy") {
        suggestion = "Sunny but chill—grab a coffee and enjoy a quiet walk.";
      } else if (userMood === "active") {
        suggestion = "Clear skies! Go for a run, bike ride, or explore a new trail.";
      } else {
        suggestion = "Perfect day for a picnic or meet-up with friends at your favorite café.";
      }
    } else if (weatherType === "Clouds") {
      suggestion =
        userMood === "cozy"
          ? "Cloudy skies—curl up with some music or journaling."
          : userMood === "active"
          ? "A bit cloudy, but still good for an outdoor walk or photography session."
          : "Call a friend and chat while enjoying the cool breeze!";
    } else {
      suggestion = "Enjoy your day your way—weather can't stop your vibe!";
    }

    document.querySelector(".suggestion").innerHTML = suggestion;

    document.querySelector(".weather").style.display = "block";
    document.querySelector(".error").style.display = "none";
  }
}

searchBtn.addEventListener("click", () => {
  checkWeather(searchBox.value);
});

// Optional: Press Enter to search
searchBox.addEventListener("keypress", (e) => {
  if (e.key === "Enter") checkWeather(searchBox.value);
});
