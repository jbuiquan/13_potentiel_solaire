import { DuckDBInstance } from '@duckdb/node-api';
import fs from 'fs';
import path from 'path';

declare global {
	// eslint-disable-next-line no-var
	var duckDbPromise: Promise<DuckDBInstance> | undefined;
}

// Access the database file

// Check if the file exists
const databasePath = process.env.DATABASE_PATH ? path.resolve(process.env.DATABASE_PATH) : null;

if (!databasePath) {
	throw new Error('DATABASE_PATH is missing or invalid');
}
if (!fs.existsSync(databasePath)) {
	throw new Error('Database file not found');
}

let dbPromise: Promise<DuckDBInstance> | undefined;

function createDB(databasePath: string): Promise<DuckDBInstance> {
	return DuckDBInstance.create(databasePath, {
		access_mode: 'READ_ONLY',
	}).then(async (db) => {
		// ensure the spatial extension is installed
		const connection = await db.connect();
		await connection.run('INSTALL SPATIAL;');
		return db;
	});
}

const duckDbSingleton = async (): Promise<DuckDBInstance> => {
	if (process.env.NODE_ENV === 'development') {
		// Use global variable in development for hot-reload
		if (!globalThis.duckDbPromise) {
			console.log('Create DB instance...');
			globalThis.duckDbPromise = createDB(databasePath);
		}
		return globalThis.duckDbPromise;
	} else {
		// Use module-level variable in production
		if (!dbPromise) {
			console.log('Create DB instance...');
			dbPromise = createDB(databasePath);
		}
		return dbPromise;
	}
};

export default duckDbSingleton;
