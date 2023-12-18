-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Dic 18, 2023 alle 22:39
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbtepsit`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `dipendenti_deepak_dawlehar`
--

CREATE TABLE `dipendenti_deepak_dawlehar` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cognome` varchar(100) NOT NULL,
  `pos_lavorativa` varchar(1024) NOT NULL,
  `data_assunzione` date NOT NULL,
  `indirizzo` varchar(1024) NOT NULL,
  `telefono` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `dipendenti_deepak_dawlehar`
--

INSERT INTO `dipendenti_deepak_dawlehar` (`id`, `nome`, `cognome`, `pos_lavorativa`, `data_assunzione`, `indirizzo`, `telefono`) VALUES
(1, 'Mario', 'Rossi', 'Manager', '2023-10-24', 'Via Roma 123', '555-1234'),
(2, 'Luca', 'Bianchi', 'Sviluppatore', '2023-10-25', 'Via Milano 456', '555-5678'),
(3, 'Giovanni', 'Marroni', 'Sviluppatore', '2023-10-29', 'Via Torino 1415', '555-2345'),
(4, 'Laura', 'Rosa', 'Analista', '2022-03-01', 'Via Roma', '555-6789'),
(5, 'Davide', 'Azzurri', 'Sviluppatore', '2023-10-31', 'Via Genova 1819', '555-1234'),
(6, 'Elena', 'Arancioni', 'Analista', '2023-11-01', 'Via Palermo 2021', '555-5678'),
(7, 'Riccardo', 'Verdi', 'Manager', '2023-11-02', 'Via Catania 2223', '555-9012'),
(8, 'Marco', 'Neri', 'Sviluppatore', '2023-10-27', 'Via Firenze 1011', '555-3456'),
(9, 'Sara', 'Vezzani', 'Manager', '2023-10-28', 'Via Venezia 1213', '556-9412');

-- --------------------------------------------------------

--
-- Struttura della tabella `zone_di_lavoro_deepak_dawlehar`
--

CREATE TABLE `zone_di_lavoro_deepak_dawlehar` (
  `id_zona` int(11) NOT NULL,
  `nome_zona` varchar(100) NOT NULL,
  `numero_clienti` int(11) NOT NULL,
  `id_dipendente` int(11) NOT NULL,
  `area_tot` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `zone_di_lavoro_deepak_dawlehar`
--

INSERT INTO `zone_di_lavoro_deepak_dawlehar` (`id_zona`, `nome_zona`, `numero_clienti`, `id_dipendente`, `area_tot`) VALUES
(1, 'Zona A', 100, 5, 5000),
(2, 'Zona B', 200, 6, 6000),
(3, 'Zona C', 150, 7, 4500),
(4, 'Zona D', 120, 8, 4800),
(5, 'Zona E', 180, 9, 5400),
(6, 'Zona A', 100, 9, 5000),
(7, 'Zona B', 200, 8, 6000),
(8, 'Zona C', 150, 7, 4500),
(9, 'Zona D', 120, 6, 4800),
(10, 'Zona Prova', 32, 1, 2700);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `dipendenti_deepak_dawlehar`
--
ALTER TABLE `dipendenti_deepak_dawlehar`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `zone_di_lavoro_deepak_dawlehar`
--
ALTER TABLE `zone_di_lavoro_deepak_dawlehar`
  ADD PRIMARY KEY (`id_zona`),
  ADD KEY `id_dipendente` (`id_dipendente`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `dipendenti_deepak_dawlehar`
--
ALTER TABLE `dipendenti_deepak_dawlehar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT per la tabella `zone_di_lavoro_deepak_dawlehar`
--
ALTER TABLE `zone_di_lavoro_deepak_dawlehar`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `zone_di_lavoro_deepak_dawlehar`
--
ALTER TABLE `zone_di_lavoro_deepak_dawlehar`
  ADD CONSTRAINT `id_dipendente` FOREIGN KEY (`id_dipendente`) REFERENCES `dipendenti_deepak_dawlehar` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `zone_di_lavoro_deepak_dawlehar_ibfk_1` FOREIGN KEY (`id_dipendente`) REFERENCES `dipendenti_deepak_dawlehar` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
