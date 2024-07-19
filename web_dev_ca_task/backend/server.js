const express = require('express');
const multer = require('multer');
const csvParser = require('csv-parser');
const fs = require('fs');
const cors = require('cors');

const app = express();
app.use(cors());
const upload = multer({ dest: 'uploads/' });

let groupInfo = [];
let hostelInfo = [];

app.post('/upload-group-info', upload.single('file'), (req, res) => {
    const filePath = req.file.path;
    const results = [];

    fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            groupInfo = results;
            fs.unlinkSync(filePath);
            res.json({ message: 'Group info uploaded successfully' });
        });
});

app.post('/upload-hostel-info', upload.single('file'), (req, res) => {
    const filePath = req.file.path;
    const results = [];

    fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            hostelInfo = results;
            fs.unlinkSync(filePath);
            res.json({ message: 'Hostel info uploaded successfully' });
        });
});

app.post('/allocate-rooms', (req, res) => {
    let allocations = [];

    groupInfo.forEach(group => {
        let allocated = false;
        hostelInfo.forEach(room => {
            if (!allocated && room.Gender.toLowerCase() === group.Gender.toLowerCase() && room.Capacity >= group.Members) {
                allocations.push({
                    GroupID: group.GroupID,
                    HostelName: room['Hostel Name'],
                    RoomNumber: room['Room Number'],
                    MembersAllocated: group.Members
                });
                room.Capacity -= group.Members;
                allocated = true;
            }
        });
    });

    res.json(allocations);
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
