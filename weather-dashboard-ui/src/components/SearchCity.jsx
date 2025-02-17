import React, { useState } from 'react';

const SearchCity = ({ onSearch }) => {
  const [searchCity, setSearchCity] = useState('');

  const handleSearch = () => {
    if (!searchCity.trim()) return;
    onSearch(searchCity.trim());
    setSearchCity('');
  };

  return (
    <div className="search-container">
      <input
        type="text"
        value={searchCity}
        onChange={(e) => setSearchCity(e.target.value)}
        placeholder="Enter city name"
        className="search-input"
      />
      <button onClick={handleSearch} className="search-button">Search</button>
    </div>
  );
};

export default SearchCity;
