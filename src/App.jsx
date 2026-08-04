import { useEffect, useMemo, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import MarkerClusterGroup from 'react-leaflet-cluster';

import prague from '../data/prague.json';
import vienna from '../data/vienna.json';
import budapest from '../data/budapest.json';

const cityOptions = [
  { key: 'prague', label: 'Prague', data: prague, center: [50.0875, 14.4214] },
  { key: 'vienna', label: 'Vienna', data: vienna, center: [48.2082, 16.3738] },
  { key: 'budapest', label: 'Budapest', data: budapest, center: [47.4979, 19.0402] }
];

const categoryGroups = [
  'attractions',
  'museums',
  'parks',
  'cafes',
  'local-restaurants',
  'nightlife',
  'cocktail-bars',
  'transport',
  'photo-spots',
  'hidden-gems'
];

const icon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function RecenterMap({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, 13);
  }, [center, map]);
  return null;
}

function App() {
  const [activeCity, setActiveCity] = useState(cityOptions[0]);
  const [query, setQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [selectedPlace, setSelectedPlace] = useState(null);

  const filteredPlaces = useMemo(() => {
    const text = query.toLowerCase();
    return activeCity.data.filter((place) => {
      const matchesQuery = !text || place.name.toLowerCase().includes(text) || place.description.toLowerCase().includes(text);
      const matchesCategory = activeCategory === 'all' || place.categories.includes(activeCategory);
      return matchesQuery && matchesCategory;
    });
  }, [activeCity, activeCategory, query]);

  useEffect(() => {
    if (filteredPlaces.length > 0) {
      setSelectedPlace(filteredPlaces[0]);
    } else {
      setSelectedPlace(null);
    }
  }, [filteredPlaces]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(255,90,95,0.14),_transparent_28%),linear-gradient(135deg,_#f9f2e8_0%,_#f3ebe1_100%)] p-4 lg:p-6">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 lg:flex-row">
        <aside className="w-full rounded-[28px] border border-stone-200 bg-white/90 p-5 shadow-[0_25px_70px_rgba(23,34,51,0.12)] backdrop-blur lg:w-[380px] lg:sticky lg:top-4 lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto">
          <div className="flex items-center gap-3 border-b border-stone-200 pb-4">
            <div className="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-rose-500 to-sky-500 text-xl text-white shadow-lg">✦</div>
            <div>
              <h1 className="text-lg font-semibold">Ultimate Central Europe Guide</h1>
              <p className="text-sm text-stone-500">Trip-inspired discovery for Prague, Vienna & Budapest</p>
            </div>
          </div>

          <div className="mt-4 space-y-4">
            <div>
              <h2 className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-stone-500">Cities</h2>
              <div className="grid gap-2">
                {cityOptions.map((city) => (
                  <button
                    key={city.key}
                    onClick={() => {
                      setActiveCity(city);
                      setActiveCategory('all');
                      setQuery('');
                    }}
                    className={`rounded-2xl border px-4 py-3 text-left text-sm font-semibold transition ${activeCity.key === city.key ? 'border-sky-300 bg-sky-50 text-sky-700' : 'border-stone-200 bg-white text-stone-700 hover:border-sky-200'}`}
                  >
                    {city.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold uppercase tracking-[0.2em] text-stone-500">Search</label>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search spots, food, nightlife..."
                className="w-full rounded-2xl border border-stone-200 bg-stone-50 px-3 py-3 text-sm outline-none focus:border-sky-400"
              />
            </div>

            <div>
              <h2 className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-stone-500">Filters</h2>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => setActiveCategory('all')} className={`rounded-full border px-3 py-2 text-xs font-semibold ${activeCategory === 'all' ? 'border-rose-300 bg-rose-50 text-rose-600' : 'border-stone-200 bg-white text-stone-600'}`}>All</button>
                {categoryGroups.map((category) => (
                  <button
                    key={category}
                    onClick={() => setActiveCategory(category)}
                    className={`rounded-full border px-3 py-2 text-xs font-semibold capitalize ${activeCategory === category ? 'border-sky-300 bg-sky-50 text-sky-700' : 'border-stone-200 bg-white text-stone-600'}`}
                  >
                    {category.replace('-', ' ')}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between">
                <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-stone-500">Places</h2>
                <span className="text-sm text-stone-500">{filteredPlaces.length}</span>
              </div>
              <div className="space-y-3">
                {filteredPlaces.map((place) => (
                  <button
                    key={place.id}
                    onClick={() => setSelectedPlace(place)}
                    className={`w-full rounded-3xl border bg-white p-3 text-left shadow-sm transition ${selectedPlace?.id === place.id ? 'border-sky-300 ring-2 ring-sky-100' : 'border-stone-200 hover:border-sky-200'}`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h3 className="text-sm font-semibold text-stone-800">{place.name}</h3>
                        <p className="mt-1 text-xs text-stone-500">{place.address}</p>
                      </div>
                      <span className="rounded-full bg-amber-100 px-2.5 py-1 text-[11px] font-semibold text-amber-700">★ {place.rating}</span>
                    </div>
                    <img src={place.image} alt={place.name} className="mt-3 h-24 w-full rounded-2xl object-cover" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </aside>

        <main className="flex-1 rounded-[28px] border border-stone-200 bg-white/90 p-3 shadow-[0_25px_70px_rgba(23,34,51,0.12)] backdrop-blur lg:p-4">
          <div className="mb-3 rounded-[24px] border border-stone-200 bg-stone-50 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-stone-500">Now exploring</p>
                <h2 className="text-xl font-semibold text-stone-900">{activeCity.label}</h2>
              </div>
              {selectedPlace && (
                <div className="max-w-xl rounded-2xl border border-stone-200 bg-white p-3 text-sm text-stone-600">
                  <div className="font-semibold text-stone-800">{selectedPlace.name}</div>
                  <div className="mt-1">{selectedPlace.description}</div>
                </div>
              )}
            </div>
          </div>

          <div className="h-[70vh] min-h-[520px] overflow-hidden rounded-[24px] border border-stone-200">
            <MapContainer center={activeCity.center} zoom={13} scrollWheelZoom className="h-full w-full">
              <RecenterMap center={activeCity.center} />
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <MarkerClusterGroup chunkedLoading>
                {filteredPlaces.map((place) => (
                  <Marker
                    key={place.id}
                    position={[place.lat, place.lng]}
                    icon={icon}
                    eventHandlers={{ click: () => setSelectedPlace(place) }}
                  >
                    <Popup>
                      <div className="space-y-2">
                        <div className="font-semibold">{place.name}</div>
                        <div className="text-sm text-stone-600">{place.address}</div>
                        <div className="text-xs text-stone-500">{place.openingHours || 'Open daily'}</div>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </MarkerClusterGroup>
            </MapContainer>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
