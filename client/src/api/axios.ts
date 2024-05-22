import axios from 'axios';
import { addError } from '$s/errors';

// Interfaz para definir la estructura de los errores de la API
interface ApiError {
	message: string; // Mensaje descriptivo del error
	error: string;   // Código o identificador del error
}

// Crear una instancia de Axios con una URL base
export const api = axios.create({
	baseURL: '/api' // Establece la URL base para todas las solicitudes de la instancia de Axios
});

// Interceptores de respuesta para manejar errores globales
api.interceptors.response.use(
	// Si la respuesta es exitosa, simplemente la devuelve
	(res) => res,
	// Si hay un error en la respuesta
	(err) => {
		// Si la respuesta tiene un código de estado 500 o superior (errores del servidor)
		if (err.response && err.response.status >= 500) {
			const { response } = err;
			const message = getErrorMessage(err);

			// Si hay un mensaje de error, agrega el error al store de errores
			if (message) {
				addError({
					contentType: response.headers['Content-Type'] || response.headers['content-type'],
					message: getErrorMessage(err)
				});
			}
		}
		// Rechaza la promesa con el error para que pueda ser manejado más adelante
		return Promise.reject(err);
	}
);

// Función para obtener el mensaje de error de una respuesta de Axios
export const getErrorMessage = (error: unknown) => {
	if (axios.isAxiosError(error)) {
		const apiError = error.response?.data as ApiError;
		if (typeof apiError === 'string' && (apiError as string).length > 0) {
			return apiError;
		}
		return apiError?.message || apiError?.error || error.message;
	}

	if (error instanceof Error) {
		return error.message;
	}

	if (error && typeof error === 'object' && 'message' in error && typeof error.message === 'string') {
		return error.message;
	}

	return 'Something went wrong'; // Mensaje genérico en caso de no poder determinar el error
};

// Función para obtener el error completo de una respuesta de Axios
export const getError = (error: unknown) => {
	if (axios.isAxiosError(error)) {
		const apiError = error.response?.data as ApiError;
		return apiError;
	}

	return null; // Retorna null si no es un error de Axios
};
