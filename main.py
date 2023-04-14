import socket
from qiskit import QuantumCircuit, execute, Aer
from qiskit.providers.ibmq import least_busy, IBMQ
from qiskit.providers.exceptions import JobError
from config import API_TOKEN

IBMQ.save_account(
    API_TOKEN,
    overwrite=True)
bit_length = 20

def internet_connection_available():
    try:
        print("Überprüfe Internetverbindung...")
        socket.create_connection(("www.google.com", 80))
        print("Internetverbindung ist verfügbar. ⚡️")
        return True
    except OSError:
        print("Internetverbindung ist nicht verfügbar! 🚨 Verwende den lokalen QASM Simulator...")
        return False

def generate_random_number(bit_length, use_ibmq=None):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    use_ibmq = internet_connection_available() if use_ibmq is None else use_ibmq
    backend = Aer.get_backend('qasm_simulator')

    if use_ibmq:
        print("Verwende das IBM Quantum Backend ✨")
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        backend = least_busy(provider.backends(filters=lambda
            x: x.configuration().n_qubits >= 1 and not x.configuration().simulator and x.status().operational == True))

    print("Führe Quantenschaltkreis aus. Es wird magisch...")
    try:
        job = execute(qc, backend, shots=bit_length, memory=True)
        result_bits = job.result().get_memory()
    except JobError as e:
        print(f"Job-Fehler: {e}")
        exit(1)

    random_number = 0
    for i, bit in enumerate(result_bits):
        print(f"Bit {i + 1} von {bit_length}: {bit}")
        random_number |= (int(bit) << i)

    print("Wandle Ergebnisbits in Zufallszahl um.")
    return random_number

if __name__ == '__main__':
    print("Generiere Zufallszahl 🎲")
    random_number = generate_random_number(bit_length)
    print(f"Die Zufallszahl ({bit_length} bits): {random_number}")
