import axios from 'axios';

const api = axios.create ({
    baseURL: 'http://0.0.0.0:8000/api/'
})

export async function uploadModel(model) {
    try {
        const response = await api.post('upload-model', model, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw new Error(error);
    }
}

export async function submitData(data) {
    try {
        const response = await api.post('predict', data);
        console.log(response);
        return response.data;
    } catch (error) {
        throw new Error(error);
    }
}