import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const FileUploadComponent = () => {
    const [groupFile, setGroupFile] = useState(null);
    const [hostelFile, setHostelFile] = useState(null);
    const [allocations, setAllocations] = useState([]);

    const onDropGroupFile = (acceptedFiles) => {
        setGroupFile(acceptedFiles[0]);
    };

    const onDropHostelFile = (acceptedFiles) => {
        setHostelFile(acceptedFiles[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', groupFile);

        await axios.post('http://localhost:3001/upload-group-info', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        formData.set('file', hostelFile);
        await axios.post('http://localhost:3001/upload-hostel-info', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        const response = await axios.post('http://localhost:3001/allocate-rooms');
        setAllocations(response.data);
    };

    const { getRootProps: getGroupRootProps, getInputProps: getGroupInputProps } = useDropzone({ onDrop: onDropGroupFile });
    const { getRootProps: getHostelRootProps, getInputProps: getHostelInputProps } = useDropzone({ onDrop: onDropHostelFile });

    return (
        <div>
            <div {...getGroupRootProps()}>
                <input {...getGroupInputProps()} />
                <p>Drag 'n' drop group info CSV file here, or click to select file</p>
            </div>
            <div {...getHostelRootProps()}>
                <input {...getHostelInputProps()} />
                <p>Drag 'n' drop hostel info CSV file here, or click to select file</p>
            </div>
            <button onClick={handleUpload}>Upload Files</button>
            <div>
                <h2>Allocation Results</h2>
                <ul>
                    {allocations.map((allocation, index) => (
                        <li key={index}>
                            Group ID: {allocation.GroupID}, Hostel Name: {allocation.HostelName}, Room Number: {allocation.RoomNumber}, Members Allocated: {allocation.MembersAllocated}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

const App = () => {
    return (
        <div className="App">
            <h1>Hostel Room Allocation</h1>
            <FileUploadComponent />
        </div>
    );
};

export default App;
