-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 15, 2025 at 04:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `biblioteca`
--

-- --------------------------------------------------------

--
-- Table structure for table `carti`
--

CREATE TABLE `carti` (
  `id` int(11) NOT NULL,
  `cod_bare` varchar(50) NOT NULL,
  `titlu` varchar(255) NOT NULL,
  `autor` varchar(255) DEFAULT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `cota` varchar(50) DEFAULT NULL,
  `raft` varchar(10) DEFAULT NULL,
  `nivel` varchar(10) DEFAULT NULL,
  `pozitie` varchar(10) DEFAULT NULL,
  `locatie_completa` varchar(100) GENERATED ALWAYS AS (concat('Raft ',`raft`,' - Nivel ',`nivel`,' - Poziția ',`pozitie`)) STORED,
  `sectiune` varchar(50) DEFAULT NULL,
  `observatii_locatie` text DEFAULT NULL,
  `data_adaugare` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_romanian_ci;

--
-- Dumping data for table `carti`
--

INSERT INTO `carti` (`id`, `cod_bare`, `titlu`, `autor`, `isbn`, `cota`, `raft`, `nivel`, `pozitie`, `sectiune`, `observatii_locatie`, `data_adaugare`) VALUES
(1, 'BOOK001', 'Amintiri din copilărie', 'Ion Creangă', '9789734640539', '821.135.1 CRE a', 'A', '1', '01', 'Literatură română', NULL, '2025-11-15 09:26:52'),
(2, 'BOOK002', 'Maitreyi000', 'Mircea Eliade', '9789734640546', '821.135.1 ELI m', 'A', '1', '02', 'Literatură română', '', '2025-11-15 09:26:52'),
(3, 'BOOK003', 'Pădurea spânzuraților', 'Liviu Rebreanu', '9789734640553', '821.135.1 REB p', 'A', '1', '03', 'Literatură română', NULL, '2025-11-15 09:26:52'),
(4, 'BOOK004', 'Enigma Otiliei99', 'George Călinescu', '9789734640560', '821.135.1 CAL e', 'A', '1', '04', 'Literatură română', '', '2025-11-15 09:26:52'),
(5, 'BOOK005', 'Moromeții', 'Marin Preda', '9789734640577', '821.135.1 PRE m', 'A', '1', '05', 'Literatură română', NULL, '2025-11-15 09:26:52'),
(6, 'BOOK006', 'Bebe', 'Autor Bebe', '235456565', 'SL455', 'P', '1', '05', 'Filosofie', '', '2025-11-15 09:36:17');

-- --------------------------------------------------------

--
-- Table structure for table `cititori`
--

CREATE TABLE `cititori` (
  `id` int(11) NOT NULL,
  `cod_bare` varchar(50) NOT NULL,
  `nume` varchar(100) NOT NULL,
  `prenume` varchar(100) NOT NULL,
  `telefon` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `data_inregistrare` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_romanian_ci;

--
-- Dumping data for table `cititori`
--

INSERT INTO `cititori` (`id`, `cod_bare`, `nume`, `prenume`, `telefon`, `email`, `data_inregistrare`) VALUES
(1, 'USER001', 'Popescuffff', 'Ion', '0721123456', 'ion.popescu@email.ro', '2025-11-15 09:26:52'),
(2, 'USER002', 'Ionescu', 'Maria', '0722234567', 'maria.ionescu@email.ro', '2025-11-15 09:26:52'),
(3, 'USER003', 'Dumitrescu', 'Andrei', '0723345678', 'andrei.dumitrescu@email.ro', '2025-11-15 09:26:52');

-- --------------------------------------------------------

--
-- Table structure for table `imprumuturi`
--

CREATE TABLE `imprumuturi` (
  `id` int(11) NOT NULL,
  `cod_cititor` varchar(50) NOT NULL,
  `cod_carte` varchar(50) NOT NULL,
  `data_imprumut` timestamp NOT NULL DEFAULT current_timestamp(),
  `data_returnare` timestamp NULL DEFAULT NULL,
  `status` enum('activ','returnat') DEFAULT 'activ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_romanian_ci;

-- --------------------------------------------------------

--
-- Table structure for table `istoric_locatii`
--

CREATE TABLE `istoric_locatii` (
  `id` int(11) NOT NULL,
  `cod_carte` varchar(50) NOT NULL,
  `raft_vechi` varchar(10) DEFAULT NULL,
  `nivel_vechi` varchar(10) DEFAULT NULL,
  `pozitie_veche` varchar(10) DEFAULT NULL,
  `raft_nou` varchar(10) DEFAULT NULL,
  `nivel_nou` varchar(10) DEFAULT NULL,
  `pozitie_noua` varchar(10) DEFAULT NULL,
  `data_mutare` timestamp NOT NULL DEFAULT current_timestamp(),
  `utilizator` varchar(100) DEFAULT NULL,
  `motiv` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_romanian_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `carti`
--
ALTER TABLE `carti`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cod_bare` (`cod_bare`),
  ADD KEY `idx_cod_bare` (`cod_bare`),
  ADD KEY `idx_locatie` (`raft`,`nivel`,`pozitie`),
  ADD KEY `idx_cota` (`cota`);

--
-- Indexes for table `cititori`
--
ALTER TABLE `cititori`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cod_bare` (`cod_bare`),
  ADD KEY `idx_cod_bare` (`cod_bare`);

--
-- Indexes for table `imprumuturi`
--
ALTER TABLE `imprumuturi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cod_carte` (`cod_carte`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_cititor` (`cod_cititor`);

--
-- Indexes for table `istoric_locatii`
--
ALTER TABLE `istoric_locatii`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cod_carte` (`cod_carte`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `carti`
--
ALTER TABLE `carti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `cititori`
--
ALTER TABLE `cititori`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `imprumuturi`
--
ALTER TABLE `imprumuturi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `istoric_locatii`
--
ALTER TABLE `istoric_locatii`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `imprumuturi`
--
ALTER TABLE `imprumuturi`
  ADD CONSTRAINT `imprumuturi_ibfk_1` FOREIGN KEY (`cod_cititor`) REFERENCES `cititori` (`cod_bare`),
  ADD CONSTRAINT `imprumuturi_ibfk_2` FOREIGN KEY (`cod_carte`) REFERENCES `carti` (`cod_bare`);

--
-- Constraints for table `istoric_locatii`
--
ALTER TABLE `istoric_locatii`
  ADD CONSTRAINT `istoric_locatii_ibfk_1` FOREIGN KEY (`cod_carte`) REFERENCES `carti` (`cod_bare`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
