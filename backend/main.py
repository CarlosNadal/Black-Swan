import React, { useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import axios from 'axios';

export default function BlackSwanRecon() {
  const [data, setData] = useState({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);

  useEffect(() => {
    axios.get('/api/recon')
      .then(res => {
        const aps = res.data.aps;
        const nodes = [];
        const links = [];

        aps.forEach(ap => {
          nodes.push({ id: ap.bssid, name: ap.essid, type: 'ap' });
          ap.clients.forEach(client => {
            nodes.push({ id: client.mac, type: 'client' });
            links.push({ source: ap.bssid, target: client.mac });
          });
        });
        setData({ nodes, links });
      })
      .catch(err => console.error(err));
  }, []);

  const handleNodeRightClick = (node, event) => {
    setSelectedNode(node);
    setContextMenu({ x: event.clientX, y: event.clientY });
  };

  const handleAttack = (type) => {
    if (!selectedNode) return;

    const payload = {
      type,
      target: selectedNode.id
    };

    axios.post('/api/attack', payload)
      .then(() => alert(`🚀 Ataque ${type} lanzado contra ${selectedNode.id}`))
      .catch(err => alert(`❌ Error: ${err.message}`));

    setContextMenu(null);
  };

  return (
    <div style={{ backgroundColor: '#111', height: '100vh', color: 'cyan', padding: 10 }}>
      <h2 style={{ color: 'cyan', textAlign: 'center' }}>Black Swan – WiFi Recon</h2>
      <ForceGraph2D
        graphData={data}
        nodeLabel="id"
        nodeAutoColorBy="type"
        onNodeRightClick={handleNodeRightClick}
      />

      {contextMenu && (
        <div
          style={{
            position: 'absolute',
            top: contextMenu.y,
            left: contextMenu.x,
            backgroundColor: '#222',
            color: 'white',
            padding: '10px',
            borderRadius: '8px',
            boxShadow: '0 0 10px rgba(0,255,255,0.5)',
            zIndex: 1000
          }}
        >
          <div style={{ marginBottom: 5 }}>🎯 Ataques disponibles:</div>
          <button onClick={() => handleAttack('deauth')}>💣 Deauth</button><br />
          <button onClick={() => handleAttack('handshake')}>💍 Handshake</button><br />
          <button onClick={() => handleAttack('crack')}>🔓 Crackeo</button><br />
          <button onClick={() => setContextMenu(null)}>❌ Cancelar</button>
        </div>
      )}
    </div>
  );
}
