const express = require("express");
const cors = require("cors");
const { SerialPort } = require("serialport"); // ✅ Correct import
const { ReadlineParser } = require("@serialport/parser-readline"); // ✅ Correct import

const PORT_NAME = "/dev/cu.usbmodem1301"; // Change this to match your Arduino port
const BAUD_RATE = 115200; // GRBL default baud rate

const app = express();
app.use(cors());
app.use(express.json());

// Initialize SerialPort for Arduino (GRBL)
const port = new SerialPort({ path: PORT_NAME, baudRate: BAUD_RATE }); // ✅ Updated syntax
const parser = port.pipe(new ReadlineParser({ delimiter: "\n" })); // ✅ Corrected Parser

// Handle incoming serial data (GRBL responses)
parser.on("data", (data) => {
    console.log("GRBL Response:", data.trim());
});

// Send a "?" command every second to keep GRBL alive
setInterval(() => {
    port.write("?\n");
}, 1000);

// API route to send G-code to GRBL
app.post("/send", (req, res) => {
    const { command } = req.body;

    if (!command) {
        return res.status(400).send("No command received.");
    }

    console.log("Sending to GRBL:", command);
    port.write(command + "\n", (err) => {
        if (err) {
            return res.status(500).send("Error writing to serial port.");
        }
        res.send("G-code sent: " + command);
    });
});

// Start server
const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));