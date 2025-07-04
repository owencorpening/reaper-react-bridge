import React, { useState, useEffect } from 'react';

function DelayEffectUI() {
  const [settings, setSettings] = useState({
    delayTime: 500,
    feedback: 0.7,
    wetDryMix: 0.5
  });

  useEffect(() => {
    if (window.wwr_start) {
      window.wwr_start();
      console.log('Webctl initialized');
    }
  }, []);

  const sendSettings = () => {
    const payload = {
      effectId: 'myCustomDelay',
      settings
    };
    const jsonString = JSON.stringify(payload);
    if (window.wwr_req) {
      window.wwr_req(`SET/EFFECT/SETTINGS?data=${encodeURIComponent(jsonString)}`);
    }
  };

  const handleChange = (key) => (e) => {
    const value = parseFloat(e.target.value);
    setSettings(prev => ({ ...prev, [key]: value }));
    sendSettings();
  };

  return (
    <div>
      <h1>My Custom Delay</h1>
      <label>
        Delay Time (ms):
        <input type="range" min="0" max="1000" value={settings.delayTime} onChange={handleChange('delayTime')} />
        {settings.delayTime}
      </label>
      <label>
        Feedback:
        <input type="range" min="0" max="1" step="0.01" value={settings.feedback} onChange={handleChange('feedback')} />
        {settings.feedback}
      </label>
      <label>
        Wet/Dry Mix:
        <input type="range" min="0" max="1" step="0.01" value={settings.wetDryMix} onChange={handleChange('wetDryMix')} />
        {settings.wetDryMix}
      </label>
    </div>
  );
}

export default DelayEffectUI;
