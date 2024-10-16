import React, {useState} from 'react';
import './ImageHandler.css';
import {SnackbarProvider, useSnackbar} from 'notistack';

const ImageHandler: React.FC = () => {
    const {enqueueSnackbar} = useSnackbar();

    const [imageSrc, setImageSrc] = useState('');
    const [identified, setIdentified] = useState<any>();

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadMessage, setUploadMessage] = useState<string>('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setSelectedFile(file);
            setUploadMessage('');

            setImageSrc('');
            setIdentified(null);
        } else {
            setSelectedFile(null);
            setUploadMessage('Please select a valid image file.');
        }
    };

    const updatePath = (givenPath:any) => `http://localhost:5007/${givenPath.replace(/\\/g, '/').replace(/^\.\.\//, '')}`;

    const handleUpload = async () => {
        if (!selectedFile) {
            setUploadMessage('No file selected');
            return;
        }

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('http://localhost:5007/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                setUploadMessage(`Error uploading image: ${errorData.error}`);
            } else {
                const data = await response.json();

                setImageSrc(updatePath(data.image_path));

                fetch("http://127.0.0.1:5007/classify", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Success:', data);
                        setIdentified(data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        enqueueSnackbar('Error:'+ error, {variant: 'error'});
                    });
                setUploadMessage(`Image uploaded successfully`);
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            setUploadMessage('Unexpected error occurred during upload.');
        }
    };

    const formatString = (str:any) => str.replace(/_+/g, ' ');

    return (
        <div className="upload-container">

            <h1 className="title">Traffic Sign Recognition System</h1>
            <input type="file" className="file-input" accept="image/*" onChange={handleFileChange} />
            <button className="upload-button" onClick={handleUpload}>Upload</button>
            {uploadMessage && <p className="upload-message">{uploadMessage}</p>}

            {imageSrc && (
                <div className="img-container">
                    <img src={imageSrc} alt="Uploaded" style={{width: '300px', height: 'auto'}}/>
                </div>
            )}
            {identified &&
                <div>
                    <label><b>Sign:</b>&nbsp;&nbsp;</label>
                    <label>{identified.sign}</label>
                </div>
            }
        </div>
    );
};

export default ImageHandler;
