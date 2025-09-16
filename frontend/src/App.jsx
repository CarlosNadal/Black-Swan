import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import "./App.css";

function App() {
  const svgRef = useRef();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/recon")
      .then((res) => res.json())
      .then(setData);
  }, []);

  useEffect(() => {
    if (!data) return;

    const width = 900;
    const height = 600;
    const nodes = [];
    const links = [];

    data.aps.forEach((ap) => {
      nodes.push({ id: ap.bssid, label: ap.essid || ap.bssid, type: "ap" });
      ap.clients.forEach((client) => {
        nodes.push({ id: client.mac, label: client.mac, type: "client" });
        links.push({ source: ap.bssid, target: client.mac });
      });
    });

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    svg.selectAll("*").remove(); // limpiar

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .attr("stroke", "#aaa")
      .selectAll("line")
      .data(links)
      .join("line");

    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 20)
      .attr("fill", d => d.type === "ap" ? "#00bcd4" : "#4caf50")
      .call(drag(simulation));

    const label = svg.append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .text(d => d.label)
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .attr("font-size", "10px");

    simulation.on("tick", () => {
      node.attr("cx", d => d.x).attr("cy", d => d.y);
      label.attr("x", d => d.x).attr("y", d => d.y);
      link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
    });

    function drag(simulation) {
      return d3.drag()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        });
    }
  }, [data]);

  return (
    <div className="App">
      <h1>Black Swan — WiFi Recon</h1>
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default App;
