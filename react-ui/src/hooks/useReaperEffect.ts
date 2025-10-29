import { useState, useEffect, useCallback, useRef } from 'react';

interface UseReaperEffectReturn {
  connected: boolean;
  sendParam: (param: string, value: number) => void;
  currentValues: Record<string, number>;
  error: string | null;
}

export function useReaperEffect(effectName: string): UseReaperEffectReturn {
  const [connected, setConnected] = useState(false);
  const [currentValues, setCurrentValues] = useState<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  
  const connect = useCallback(() => {
    const ws = new WebSocket('ws://localhost:8765/ws');
    
    ws.onopen = () => {
      setConnected(true);
      setError(null);
    };
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'param_update' && message.effect === effectName) {
        setCurrentValues(prev => ({ ...prev, [message.param]: message.value }));
      }
    };
    
    ws.onclose = () => {
      setConnected(false);
      setTimeout(() => connect(), 3000);
    };
    
    wsRef.current = ws;
  }, [effectName]);
  
  const sendParam = useCallback((param: string, value: number) => {
    wsRef.current?.send(JSON.stringify({
      type: 'set_param',
      effect: effectName,
      param,
      value
    }));
  }, [effectName]);
  
  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);
  
  return { connected, sendParam, currentValues, error };
}
