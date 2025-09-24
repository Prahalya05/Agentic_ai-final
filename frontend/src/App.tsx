import React, { useState } from 'react';
import './App.css';

type ItineraryActivity = { time: string; item: string; details: string };
type ItineraryDay = { day: number; activities: ItineraryActivity[] };

type ApiResponse = {
  location: string;
  user_prefs: Record<string, unknown>;
  attractions: { name: string; description: string; category?: string }[];
  foods: { name: string; description: string; type?: string }[];
  itinerary: ItineraryDay[];
  narration: string[];
  evaluation_score: number;
};

function App() {
  const [location, setLocation] = useState('');
  const [days, setDays] = useState(3);
  const [style, setStyle] = useState('fun');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ApiResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location,
          user_prefs: { duration: days, style },
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Request failed');
      }
      const json = (await res.json()) as ApiResponse;
      setData(json);
    } catch (e: any) {
      setError(e?.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <nav className="nav">
        <div className="brand">AI Travel Vlogger</div>
      </nav>

      <div className="controls">
        <input
          className="input"
          placeholder="Enter a location (e.g., Tokyo)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <input
          className="number"
          type="number"
          min={1}
          max={10}
          value={days}
          onChange={(e) => setDays(parseInt(e.target.value || '1', 10))}
        />
        <select className="select" value={style} onChange={(e) => setStyle(e.target.value)}>
          <option value="fun">Fun</option>
          <option value="luxury">Luxury</option>
          <option value="budget">Budget</option>
          <option value="foodie">Foodie</option>
        </select>
        <button className="button" onClick={handleGenerate} disabled={!location || loading}>
          {loading ? 'Generating…' : 'Generate'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {data && (
        <div className="timeline">
          {data.itinerary?.map((day, idx) => (
            <div key={day.day} className="card">
              <div className="card-header">Day {day.day}</div>
              <div className="card-body">
                <ul className="activities">
                  {day.activities.map((a, i) => (
                    <li key={i}>
                      <span className="time">{a.time}</span>
                      <span className="item">{a.item}</span>
                      <span className="details">{a.details}</span>
                    </li>
                  ))}
                </ul>
                {data.narration?.[idx] && (
                  <div className="narration">{data.narration[idx]}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
