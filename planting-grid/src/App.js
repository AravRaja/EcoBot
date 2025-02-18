import React, { useState } from "react";
import "./Grid.css"; // Styling for grid

const GRID_SIZE = 15; // 15x15 Grid
const CNC_MAX = 50; // Max area now 30x30 instead of 300x300
const CELL_SIZE = CNC_MAX / GRID_SIZE; // Each cell represents (30/15 = 2mm)

const Grid = () => {
    // Manage grid state locally
    const [grid, setGrid] = useState(Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false)));

    // Toggle planting state
    const toggleCell = (row, col) => {
        const updatedGrid = [...grid];
        updatedGrid[row][col] = !updatedGrid[row][col];
        setGrid(updatedGrid);
    };

    // Reset the grid (clear all selections)
    const resetGrid = () => {
        setGrid(Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false)));
    };

    // Function to send G-code to Node.js backend
    const sendGCode = async (command) => {
        try {
            await fetch("http://localhost:3000/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command })
            });
        } catch (error) {
            console.error("Error sending G-code:", error);
        }
    };
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    // Generate and send G-code for planted positions
    const generateGCode = async () => {
        let gcodeCommands = [];

        // Unlock GRBL first
        await sendGCode("$X");
        await new Promise(resolve => setTimeout(resolve, 500)); // Wait 500ms for unlock
        await sendGCode("G92 X0 Y0"); // Set current position as (0,0)

        for (let rowIndex = 0; rowIndex < GRID_SIZE; rowIndex++) {
            for (let colIndex = 0; colIndex < GRID_SIZE; colIndex++) {
                if (grid[rowIndex][colIndex]) {
                    // Convert row/col into CNC coordinates (Scale by CELL_SIZE)
                    console.log(rowIndex, colIndex)
                    const x = rowIndex * CELL_SIZE;
                    const y = (GRID_SIZE - 1 - colIndex) * CELL_SIZE; // Reverse Y axis to match the desired orientation
                    console.log(x,y)
                    const moveCommand = `G1 X${x.toFixed(2)} Y${y.toFixed(2)} F1000`;
                    console.log(moveCommand)
                    gcodeCommands.push(moveCommand);

                    // Move to position
                    await sendGCode(moveCommand);

                    // Activate planting mechanism (M5 S90)
                    await sendGCode("M5 S90");
                    

                    // Wait 500ms for planting to complete
                    await sendGCode("G4 P0.2")

                    // Deactivate planting mechanism (M3)
                    await sendGCode("M3");
                    await sendGCode("G4 P0.2")

                    // Pause for 1 second when reaching an edge (X=30 or Y=30)
                    if (x >= CNC_MAX || y >= CNC_MAX) {
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    }
                }
            }
        }

        if (gcodeCommands.length > 0) {
            alert("Planting started! Sent G-Code:\n" + gcodeCommands.join("\n"));
        } else {
            alert("No plants selected! Click on the grid to plant seeds.");
        }
    };

    return (
        <div className="grid-container">
            <h2>🌿 Planting Grid (30x30 CNC)</h2>
            {grid.map((row, rowIndex) => (
                <div key={rowIndex} className="grid-row">
                    {row.map((cell, colIndex) => (
                        <button
                            key={colIndex}
                            className={`grid-cell ${cell ? "planted" : "empty"}`}
                            onClick={() => toggleCell(rowIndex, colIndex)}
                        >
                            {cell ? "🌱" : "🟫"}
                        </button>
                    ))}
                </div>
            ))}
            <br />
            <button className="reset-button" onClick={resetGrid}>Reset Grid ❌</button>
            <button className="start-button" onClick={generateGCode}>Start Planting 🌾</button>
            <br />
            <a href="http://localhost:8501">Go to Dashboard 📊</a> {/* Link to Streamlit */}
        </div>
    );
};

export default Grid;
