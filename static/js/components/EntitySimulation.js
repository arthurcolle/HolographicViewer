import React, { useState, useEffect } from 'react';

const EntitySimulation = () => {
  const [entities, setEntities] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [systemStatus] = useState({
    temperature: 36,
    syncRatio: 98.5,
    secure: true
  });
  
  // Fetch entities from API
  useEffect(() => {
    fetch('/entities')
      .then(response => response.json())
      .then(data => {
        setEntities(data);
      })
      .catch(error => {
        console.error("Failed to fetch entities:", error);
      });
  }, []);
  
  // Handle entity selection
  const handleSelectEntity = (entityId) => {
    setSelectedEntity(entities.find(e => e.entity_id === entityId));
  };
  
  // Format date for display
  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleString();
  };
  
  return (
    <div className="w-full h-screen bg-black text-amber-400 font-mono overflow-hidden">
      {/* Holographic Grid Effect (CSS overlay) */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="w-full h-full opacity-30" 
          style={{
            backgroundImage: "linear-gradient(to right, #ffb300 1px, transparent 1px), linear-gradient(to bottom, #ffb300 1px, transparent 1px)",
            backgroundSize: "50px 50px"
          }}
        ></div>
        <div className="w-full h-full opacity-20"
          style={{
            background: "repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1) 1px, transparent 1px, transparent 2px)"
          }}
        ></div>
      </div>
      
      {/* UI Overlay */}
      <div className="absolute top-0 left-0 w-full h-full flex flex-col p-4">
        {/* Header */}
        <div className="bg-black bg-opacity-70 border border-amber-400 rounded p-4 mb-4">
          <h1 className="text-xl">ENTITY MANAGEMENT SYSTEM</h1>
          <div className="flex justify-between text-sm">
            <div>ENTITIES LOADED: {entities.length}</div>
            <div>SYSTEM STATUS: NOMINAL</div>
          </div>
        </div>
        
        {/* Main Content */}
        <div className="flex-1 flex gap-4">
          {/* Left Panel - Entity List */}
          <div className="w-64 bg-black bg-opacity-70 border border-amber-400 rounded p-4 overflow-y-auto">
            <h2 className="mb-4 border-b border-amber-400 pb-2">ENTITY CATALOG</h2>
            
            {entities.map(entity => (
              <div 
                key={entity.entity_id}
                className={`mb-2 p-2 border cursor-pointer ${
                  selectedEntity?.entity_id === entity.entity_id
                    ? 'border-cyan-400 bg-cyan-900 bg-opacity-30'
                    : 'border-amber-400 hover:bg-amber-900 hover:bg-opacity-20'
                }`}
                onClick={() => handleSelectEntity(entity.entity_id)}
              >
                <div className="font-bold truncate">{entity.description || entity.entity_id}</div>
                <div className="text-xs flex justify-between">
                  <span>{entity.ontology?.platform_type || 'Unknown Type'}</span>
                  <span className={`inline-block w-3 h-3 rounded-full ${
                    entity.health?.health_status === 1 ? 'bg-green-500' : 
                    entity.health?.health_status === 3 ? 'bg-yellow-500' : 
                    entity.health?.health_status === 2 ? 'bg-red-500' : 'bg-gray-500'
                  }`}></span>
                </div>
              </div>
            ))}
          </div>
          
          {/* Right Panel - Entity Details */}
          {selectedEntity ? (
            <div className="flex-1 bg-black bg-opacity-70 border border-amber-400 rounded p-4 overflow-y-auto">
              <div className="flex justify-between items-center mb-4 border-b border-amber-400 pb-2">
                <h2>{selectedEntity.description || selectedEntity.entity_id}</h2>
                <div className="flex">
                  <button 
                    className={`px-3 py-1 mr-2 ${activeTab === 'overview' ? 'bg-amber-400 text-black' : 'border border-amber-400'}`}
                    onClick={() => setActiveTab('overview')}
                  >
                    Overview
                  </button>
                  <button 
                    className={`px-3 py-1 mr-2 ${activeTab === 'location' ? 'bg-amber-400 text-black' : 'border border-amber-400'}`}
                    onClick={() => setActiveTab('location')}
                  >
                    Location
                  </button>
                  <button 
                    className={`px-3 py-1 ${activeTab === 'sensors' ? 'bg-amber-400 text-black' : 'border border-amber-400'}`}
                    onClick={() => setActiveTab('sensors')}
                  >
                    Sensors
                  </button>
                </div>
              </div>
              
              {activeTab === 'overview' && (
                <div>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="p-2 border border-amber-400">
                      <div className="text-sm opacity-70">ID</div>
                      <div>{selectedEntity.entity_id}</div>
                    </div>
                    <div className="p-2 border border-amber-400">
                      <div className="text-sm opacity-70">CREATED</div>
                      <div>{formatDate(selectedEntity.created_time)}</div>
                    </div>
                    <div className="p-2 border border-amber-400">
                      <div className="text-sm opacity-70">TYPE</div>
                      <div>{selectedEntity.ontology?.platform_type || 'Unknown'}</div>
                    </div>
                    <div className="p-2 border border-amber-400">
                      <div className="text-sm opacity-70">SPECIFIC TYPE</div>
                      <div>{selectedEntity.ontology?.specific_type || 'Unknown'}</div>
                    </div>
                  </div>
                  
                  <div className="border border-amber-400 p-2 mb-4">
                    <div className="text-sm opacity-70 mb-2">STATUS</div>
                    <div className="flex items-center">
                      <span className={`inline-block w-3 h-3 rounded-full mr-2 ${
                        selectedEntity.health?.health_status === 1 ? 'bg-green-500' : 
                        selectedEntity.health?.health_status === 3 ? 'bg-yellow-500' : 
                        selectedEntity.health?.health_status === 2 ? 'bg-red-500' : 'bg-gray-500'
                      }`}></span>
                      <span>
                        {selectedEntity.health?.health_status === 1 ? 'HEALTHY' :
                         selectedEntity.health?.health_status === 3 ? 'DEGRADED' :
                         selectedEntity.health?.health_status === 2 ? 'UNHEALTHY' : 'UNKNOWN'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="border border-amber-400 p-2">
                    <div className="text-sm opacity-70 mb-2">INDICATORS</div>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="flex items-center">
                        <div className={`w-4 h-4 border ${selectedEntity.indicators?.simulated ? 'bg-amber-400' : 'border-amber-400'} mr-2`}></div>
                        <span>SIMULATED</span>
                      </div>
                      <div className="flex items-center">
                        <div className={`w-4 h-4 border ${selectedEntity.indicators?.exercise ? 'bg-amber-400' : 'border-amber-400'} mr-2`}></div>
                        <span>EXERCISE</span>
                      </div>
                      <div className="flex items-center">
                        <div className={`w-4 h-4 border ${selectedEntity.indicators?.emergency ? 'bg-amber-400' : 'border-amber-400'} mr-2`}></div>
                        <span>EMERGENCY</span>
                      </div>
                      <div className="flex items-center">
                        <div className={`w-4 h-4 border ${selectedEntity.is_live ? 'bg-amber-400' : 'border-amber-400'} mr-2`}></div>
                        <span>LIVE</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {activeTab === 'location' && (
                <div className="p-4 text-center">
                  <div className="text-xl mb-4">Location Data</div>
                  {selectedEntity.location ? (
                    <div>
                      <div className="mb-2">
                        <span className="opacity-70">LAT: </span>
                        {selectedEntity.location.position?.latitude_degrees?.toFixed(6) || 'N/A'}
                      </div>
                      <div className="mb-2">
                        <span className="opacity-70">LON: </span>
                        {selectedEntity.location.position?.longitude_degrees?.toFixed(6) || 'N/A'}
                      </div>
                      <div>
                        <span className="opacity-70">ALT: </span>
                        {selectedEntity.location.position?.altitude_hae_meters?.__root__?.toFixed(1) || 'N/A'} m
                      </div>
                    </div>
                  ) : (
                    <div className="text-red-400">No location data available</div>
                  )}
                </div>
              )}
              
              {activeTab === 'sensors' && (
                <div className="p-4">
                  <div className="text-xl mb-4">Sensors</div>
                  {selectedEntity.sensors && selectedEntity.sensors.sensors?.length > 0 ? (
                    <div className="space-y-4">
                      {selectedEntity.sensors.sensors.map(sensor => (
                        <div key={sensor.sensor_id} className="border border-amber-400 p-2">
                          <div className="font-bold">{sensor.sensor_description || sensor.sensor_id}</div>
                          <div className="text-sm">
                            <div><span className="opacity-70">ID: </span>{sensor.sensor_id}</div>
                            <div><span className="opacity-70">Type: </span>{sensor.sensor_type}</div>
                            <div><span className="opacity-70">Status: </span>
                              <span className={
                                sensor.operational_state === 4 ? 'text-green-400' :
                                sensor.operational_state === 3 ? 'text-yellow-400' :
                                'text-red-400'
                              }>
                                {sensor.operational_state === 4 ? 'OPERATIONAL' :
                                 sensor.operational_state === 3 ? 'DEGRADED' :
                                 sensor.operational_state === 2 ? 'NON-OPERATIONAL' :
                                 sensor.operational_state === 1 ? 'OFF' : 'UNKNOWN'}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-red-400">No sensor data available</div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="flex-1 bg-black bg-opacity-70 border border-amber-400 rounded p-4 flex items-center justify-center">
              <div className="text-center">
                <div className="text-xl mb-2">No Entity Selected</div>
                <div className="opacity-70">Select an entity from the list to view details</div>
              </div>
            </div>
          )}
        </div>
        
        {/* Footer - System Status */}
        <div className="bg-black bg-opacity-70 border border-amber-400 rounded p-2 mt-4 text-sm">
          <div className="flex justify-between">
            <div>CORE TEMPERATURE: {systemStatus.temperature}°C</div>
            <div>SYNC RATIO: {systemStatus.syncRatio}%</div>
            <div>SECURITY: {systemStatus.secure ? 'SECURE' : 'COMPROMISED'}</div>
            <div>SYSTEM TIME: {new Date().toLocaleTimeString()}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EntitySimulation;