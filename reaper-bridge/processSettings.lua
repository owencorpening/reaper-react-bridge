-- Requires dkjson in REAPER's Lua path
local json = require("dkjson")

function processSettings()
  local jsonString = reaper.GetExtState("WebControl", "EffectSettings")
  if jsonString and jsonString ~= "" then
    local data = json.decode(jsonString)
    if data and data.effectId == "myCustomDelay" then
      reaper.SetExtState("MyCustomDelay", "delayTime", tostring(data.settings.delayTime), false)
      reaper.SetExtState("MyCustomDelay", "feedback", tostring(data.settings.feedback), false)
      reaper.SetExtState("MyCustomDelay", "wetDryMix", tostring(data.settings.wetDryMix), false)
    end
    reaper.DeleteExtState("WebControl", "EffectSettings", false)
  end
  reaper.defer(processSettings)
end

processSettings()
