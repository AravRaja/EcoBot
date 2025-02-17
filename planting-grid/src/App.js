import React, { useState } from "react";
import "./Grid.css"; // Styling for grid

const GRID_SIZE = 15;

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

    // Generate G-code for planted positions
    const generateGCode = () => {
        let gcodeCommands = [];
        grid.forEach((row, rowIndex) => {
            row.forEach((cell, colIndex) => {
                if (cell) {
                    // Convert row/col into CNC coordinates (example: X=row, Y=col, scaled by 10)
                    gcodeCommands.push(`G0 X${rowIndex * 10} Y${colIndex * 10} F500`);
                }
            });
        });

        if (gcodeCommands.length > 0) {
            alert("Generated G-Code:\n" + gcodeCommands.join("\n"));
        } else {
            alert("No plants selected! Click on the grid to plant seeds.");
        }
    };

    return (
        <div className="grid-container">
            <h2>🌿 Planting Grid</h2>
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
