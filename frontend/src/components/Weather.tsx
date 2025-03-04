import { useState, useEffect, FC } from 'react';
import axios from 'axios';
import { CloudIcon, SunIcon, CloudArrowUpIcon } from '@heroicons/react/24/solid';
  
interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  wind_speed: number;
  description: string;
  prediction_high: number;
  prediction_low: number;
  rain_probability: number;
}

const Weather: FC = () => {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [city, setCity] = useState('London');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWeather = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:8000/weather/${city}`);
      setWeather(response.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching weather:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ERR_NETWORK') {
          setError('Cannot connect to the server. Please make sure the backend is running.');
        } else if (error.response?.status === 500) {
          setError('City not found or invalid API key. Please check your input.');
        } else {
          setError(error.message);
        }
      } else {
        setError('An unexpected error occurred');
      }
      setWeather(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchWeather();
  }, []);

  const getWeatherIcon = (description: string) => {
    if (description.includes('rain')) return <CloudArrowUpIcon className="h-12 w-12 text-blue-500" />;
    if (description.includes('cloud')) return <CloudIcon className="h-12 w-12 text-gray-500" />;
    return <SunIcon className="h-12 w-12 text-yellow-500" />;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchWeather();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-400 to-purple-500 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">Weather Forecast</h1>
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter city"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Search'}
              </button>
            </form>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {weather && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-blue-50 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-2xl font-semibold text-gray-800">{city}</h2>
                    <p className="text-gray-600">{weather.description}</p>
                  </div>
                  {getWeatherIcon(weather.description)}
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-600">Temperature</p>
                    <p className="text-2xl font-bold text-gray-800">{weather.temperature}°C</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Humidity</p>
                    <p className="text-2xl font-bold text-gray-800">{weather.humidity}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Wind Speed</p>
                    <p className="text-2xl font-bold text-gray-800">{weather.wind_speed} m/s</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Pressure</p>
                    <p className="text-2xl font-bold text-gray-800">{weather.pressure} hPa</p>
                  </div>
                </div>
              </div>

              <div className="bg-purple-50 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Predictions</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-gray-600">Temperature High</p>
                    <p className="text-2xl font-bold text-red-500">{weather.prediction_high}°C</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Temperature Low</p>
                    <p className="text-2xl font-bold text-blue-500">{weather.prediction_low}°C</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Rain Probability</p>
                    <p className="text-2xl font-bold text-purple-500">{(weather.rain_probability * 100).toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Weather; 