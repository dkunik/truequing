const DB_NAME = "truequing";
const DB_VERSION = 2;

const STORE_CONFIG = "config";
const STORE_ALBUM = "album";

function bitsABytes(bits) {

    const bytes = [];

    for (let i = 0; i < bits.length; i += 8) {

        let byte = 0;

        for (let bitIndex = 0; bitIndex < 8; bitIndex++) {

            const bit =
                bits[i + bitIndex] || 0;

            if (bit) {
                byte |= (1 << bitIndex);
            }

        }

        bytes.push(byte);

    }

    return bytes;

}

function bytesABase64(bytes) {

    const binario =
        String.fromCharCode(...bytes);

    return btoa(binario);

}

function abrirDB() {

    return new Promise((resolve, reject) => {

        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onupgradeneeded = function (event) {

            const db = event.target.result;

            if (!db.objectStoreNames.contains(STORE_CONFIG)) {

                db.createObjectStore(
                    STORE_CONFIG,
                    {
                        keyPath: "key",
                    }
                );

            }

            if (!db.objectStoreNames.contains(STORE_ALBUM)) {

                db.createObjectStore(
                    STORE_ALBUM,
                    {
                        keyPath: "figurita_id",
                    }
                );

            }

        };

        request.onsuccess = function () {
            resolve(request.result);
        };

        request.onerror = function () {
            reject(request.error);
        };

    });

}

async function guardarValor(key, value) {

    const db = await abrirDB();

    const tx = db.transaction(
        STORE_CONFIG,
        "readwrite"
    );

    tx.objectStore(STORE_CONFIG).put({
        key: key,
        value: value,
    });

}

async function leerValor(key) {

    const db = await abrirDB();

    return new Promise((resolve, reject) => {

        const tx = db.transaction(
            STORE_CONFIG,
            "readonly"
        );

        const request =
            tx.objectStore(STORE_CONFIG).get(key);

        request.onsuccess = function () {

            if (request.result) {
                resolve(request.result.value);
            } else {
                resolve(null);
            }

        };

        request.onerror = function () {
            reject(request.error);
        };

    });

}

async function sincronizarAlbumLocal() {

    const response = await fetch("/api/mi-album/");
    const data = await response.json();
    await guardarValor("usuario", data.usuario);
    await guardarValor("coleccion", data.coleccion);

    const db = await abrirDB();

    const tx = db.transaction(
        STORE_ALBUM,
        "readwrite"
    );

    const store = tx.objectStore(STORE_ALBUM);

    data.album.forEach(function (item) {
        store.put(item);
    });

    return data.album.length;

}

async function contarAlbumLocal() {

    const db = await abrirDB();

    return new Promise((resolve, reject) => {

        const tx = db.transaction(
            STORE_ALBUM,
            "readonly"
        );

        const request =
            tx.objectStore(STORE_ALBUM).count();

        request.onsuccess = function () {
            resolve(request.result);
        };

        request.onerror = function () {
            reject(request.error);
        };

    });

}

async function obtenerEstadoCanjeLocal() {

    console.log("obtenerEstadoCanjeLocal: inicio");

    const metadata =
        await obtenerMetadataLocal();

    console.log("metadata local:", metadata);

    const db = await abrirDB();

    return new Promise((resolve, reject) => {

        const tx = db.transaction(
            STORE_ALBUM,
            "readonly"
        );

        const store = tx.objectStore(STORE_ALBUM);

        const request = store.getAll();

        request.onsuccess = function () {

            const album = request.result;

            console.log(
                "album local leído:",
                album.length,
                "registros"
            );

            const repetidas = [];
            const faltantes = [];

            album.forEach(function (item) {

                if (item.cantidad === 0) {
                    faltantes.push(item.figurita_id);
                }

                if (item.cantidad > 1) {
                    repetidas.push(item.figurita_id);
                }

            });

            const estadoCanje = {
                usuario: metadata.usuario,
                coleccion: metadata.coleccion,
                repetidas: repetidas,
                faltantes: faltantes,
            };

            console.log("EstadoCanje local:", estadoCanje);

            resolve(estadoCanje);

        };

        request.onerror = function () {

            console.log(
                "error leyendo album local:",
                request.error
            );

            reject(request.error);

        };

    });

}

async function obtenerMetadataLocal() {

    const usuario =
        await leerValor("usuario");

    const coleccion =
        await leerValor("coleccion");

    return {
        usuario: usuario,
        coleccion: coleccion,
    };

}


async function exportarEstadoCanjeCompactoLocal() {

    const estado =
        await obtenerEstadoCanjeLocal();

    const N = 960;

    const repetidasBits =
        new Array(N).fill(0);

    const faltantesBits =
        new Array(N).fill(0);

    estado.repetidas.forEach(function (figuritaId) {
        repetidasBits[figuritaId - 1] = 1;
    });

    estado.faltantes.forEach(function (figuritaId) {
        faltantesBits[figuritaId - 1] = 1;
    });

    const repetidasBytes =
        bitsABytes(repetidasBits);

    const faltantesBytes =
        bitsABytes(faltantesBits);

    const repetidasBase64 =
        bytesABase64(repetidasBytes);

    const faltantesBase64 =
        bytesABase64(faltantesBytes);

    const estadoCanjeCompacto = {
        v: 1,
        u: estado.usuario,
        c: estado.coleccion,
        n: N,
        r: repetidasBase64,
        f: faltantesBase64,
    };

    const estadoCanjeCompactoJson =
        JSON.stringify(estadoCanjeCompacto);

    const comprimido =
        pako.deflate(estadoCanjeCompactoJson);

    const payloadFinal =
        bytesABase64(Array.from(comprimido));

    return payloadFinal;

}

function base64ABytes(texto) {

    const binario =
        atob(texto);

    const bytes = [];

    for (let i = 0; i < binario.length; i++) {
        bytes.push(
            binario.charCodeAt(i)
        );
    }

    return bytes;

}

function bytesABits(bytes, n) {

    const bits = [];

    bytes.forEach(function (byte) {

        for (let bitIndex = 0; bitIndex < 8; bitIndex++) {

            if (byte & (1 << bitIndex)) {
                bits.push(1);
            } else {
                bits.push(0);
            }

        }

    });

    return bits.slice(0, n);

}

function bitsAIds(bits) {

    const ids = [];

    bits.forEach(function (bit, indice) {

        if (bit) {
            ids.push(indice + 1);
        }

    });

    return ids;

}

function decodificarEstadoCanjeCompactoLocal(payload) {

    const comprimidoBytes =
        base64ABytes(payload);

    const jsonCompacto =
        pako.inflate(
            new Uint8Array(comprimidoBytes),
            {
                to: "string",
            }
        );

    const compacto =
        JSON.parse(jsonCompacto);

    const repetidasBytes =
        base64ABytes(compacto.r);

    const faltantesBytes =
        base64ABytes(compacto.f);

    const repetidasBits =
        bytesABits(
            repetidasBytes,
            compacto.n
        );

    const faltantesBits =
        bytesABits(
            faltantesBytes,
            compacto.n
        );

    return {
        usuario: compacto.u,
        coleccion: compacto.c,
        repetidas: bitsAIds(repetidasBits),
        faltantes: bitsAIds(faltantesBits),
    };

}

function interseccion(a, b) {
    const setB = new Set(b);
    return a.filter(x => setB.has(x));
}

async function calcularCanjeConPayloadLocal(payloadOtro) {

    const estadoMio =
        await obtenerEstadoCanjeLocal();

    const estadoOtro =
        decodificarEstadoCanjeCompactoLocal(payloadOtro);

    return {
        usuarioOtro: estadoOtro.usuario,
        yoTengoParaOtro: interseccion(
            estadoMio.repetidas,
            estadoOtro.faltantes
        ),
        otroTieneParaMi: interseccion(
            estadoOtro.repetidas,
            estadoMio.faltantes
        ),
    };

}

async function obtenerAlbumLocal() {

    const db = await abrirDB();

    return new Promise((resolve, reject) => {

        const tx = db.transaction(
            STORE_ALBUM,
            "readonly"
        );

        const store = tx.objectStore(STORE_ALBUM);

        const request = store.getAll();

        request.onsuccess = function () {
            resolve(request.result);
        };

        request.onerror = function () {
            reject(request.error);
        };

    });

}

async function obtenerListasAlbumLocal() {

    const album =
        await obtenerAlbumLocal();

    const faltantes =
        album.filter(function (item) {
            return item.cantidad === 0;
        });

    const repetidas =
        album.filter(function (item) {
            return item.cantidad > 1;
        });

    return {
        faltantes: faltantes,
        repetidas: repetidas,
    };

}
