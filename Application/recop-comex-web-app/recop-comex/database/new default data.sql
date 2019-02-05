-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2019 at 07:15 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `recop-comex`
--

--
-- Dumping data for table `user_account`
--

INSERT INTO `user_account` (`id`, `info_id`, `username`, `password`, `email_address`, `type`, `last_active`, `status`) VALUES
(1, 1, 'admin-recop', '$2b$12$aLUMJqDekK/DY8nU5c4y3O2lWmP4.af.YCWeol5Cc.nAgw6Wau7ia', 'recop.baste@gmail.com', 1, '2019-01-29 13:43:00', 'A'),
(2, 2, 'pres.baste', '$2b$12$9kebxlvRAnR/L3Jx9GIcQeDEMuIDrOMlfoIbFNv0lkhpte7RI29WC', 'pres.baste@gmail.com', 5, '2019-01-29 13:34:26', 'A'),
(3, 3, 'acad.baste', '$2b$12$9DeJoAw7WoF6GMq9d70Tnec2ALPZEuEOa1qSWEL7S.MmJEnrZJrem', 'acad.baste@gmail.com', 5, '2019-01-29 14:05:13', 'A'),
(4, 4, 'fmi.baste', '$2b$12$UtE8pwqmZK3Et9ioHkSoSODiCzNT1cRgsyQcYkhTDxlwBlgOTDs6.', 'fmi.baste@gmail.com', 5, '2019-01-29 14:07:02', 'A');

--
-- Dumping data for table `user_information`
--

INSERT INTO `user_information` (`id`, `first_name`, `middle_name`, `last_name`, `company_name`, `bio`, `gender`, `birthday`, `address`, `telephone`, `mobile_number`, `partner_thrust`) VALUES
(1, 'Ana', 'Dula', 'Manzano', 'San Sebastian College Recoletos de Cavite', 'I am the ReCOP Director.', 'F', '1998-01-21', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(2, 'Rafael', 'Something', 'Pecson', 'San Sebastian College Recoletos de Cavite', 'I am the President.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(3, 'James', 'Dexter', 'Tanquis', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Academics.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(4, 'Cristituto', 'Somebody', 'Palomar', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Finance.', 'M', '2019-01-29', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
