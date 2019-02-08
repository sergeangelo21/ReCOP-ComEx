-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 08, 2019 at 03:57 PM
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

-- --------------------------------------------------------

--
-- Table structure for table `audit_trail`
--

CREATE TABLE `audit_trail` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `affected_id` int(11) NOT NULL,
  `target` varchar(20) NOT NULL,
  `date_created` datetime NOT NULL,
  `type` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `beneficiary`
--

CREATE TABLE `beneficiary` (
  `id` int(11) NOT NULL,
  `donor_id` int(11) DEFAULT NULL,
  `beneficiary_id` int(11) DEFAULT NULL,
  `is_employed` char(1) NOT NULL,
  `income` decimal(10,2) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `donation`
--

CREATE TABLE `donation` (
  `id` int(11) NOT NULL,
  `sponsee_id` int(11) DEFAULT NULL,
  `sponsor_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `date_given` datetime NOT NULL,
  `transaction_slip` varchar(200) NOT NULL,
  `is_event` char(1) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_attachment`
--

CREATE TABLE `event_attachment` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `path` varchar(200) NOT NULL,
  `type` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_information`
--

CREATE TABLE `event_information` (
  `id` int(11) NOT NULL,
  `organizer_id` int(11) DEFAULT NULL,
  `name` varchar(30) NOT NULL,
  `description` varchar(140) NOT NULL,
  `objective` varchar(140) NOT NULL,
  `budget` decimal(10,2) NOT NULL,
  `location` varchar(50) NOT NULL,
  `event_date` datetime NOT NULL,
  `participant_no` int(11) NOT NULL,
  `min_age` int(11) NOT NULL,
  `max_age` int(11) NOT NULL,
  `thrust` int(11) NOT NULL,
  `type` int(1) NOT NULL,
  `event_status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event_participation`
--

CREATE TABLE `event_participation` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `participant_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `comment` varchar(140) DEFAULT NULL,
  `is_target` char(1) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `donation_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `in_stock` int(11) NOT NULL,
  `given` int(11) NOT NULL,
  `expired` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_type`
--

CREATE TABLE `inventory_type` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `proposal_tracker`
--

CREATE TABLE `proposal_tracker` (
  `id` int(11) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `proposed_on` datetime NOT NULL,
  `recop_accepted` datetime DEFAULT NULL,
  `fmi_signed` datetime DEFAULT NULL,
  `acad_signed` datetime DEFAULT NULL,
  `approved_on` datetime DEFAULT NULL,
  `comment` varchar(20) DEFAULT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `referral`
--

CREATE TABLE `referral` (
  `id` int(11) NOT NULL,
  `referrer_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  `type` int(1) NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_account`
--

CREATE TABLE `user_account` (
  `id` int(11) NOT NULL,
  `info_id` int(11) DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `email_address` varchar(30) NOT NULL,
  `type` int(1) NOT NULL,
  `last_active` datetime NOT NULL,
  `status` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_account`
--

INSERT INTO `user_account` (`id`, `info_id`, `username`, `password`, `email_address`, `type`, `last_active`, `status`) VALUES
(1, 1, 'admin-recop', '$2b$12$aLUMJqDekK/DY8nU5c4y3O2lWmP4.af.YCWeol5Cc.nAgw6Wau7ia', 'recop.baste@gmail.com', 1, '2019-02-07 21:49:20', 'A'),
(2, 2, 'pres.baste', '$2b$12$9kebxlvRAnR/L3Jx9GIcQeDEMuIDrOMlfoIbFNv0lkhpte7RI29WC', 'pres.baste@gmail.com', 5, '2019-01-29 13:34:26', 'A'),
(3, 3, 'acad.baste', '$2b$12$9DeJoAw7WoF6GMq9d70Tnec2ALPZEuEOa1qSWEL7S.MmJEnrZJrem', 'acad.baste@gmail.com', 5, '2019-01-29 14:05:13', 'A'),
(4, 4, 'fmi.baste', '$2b$12$UtE8pwqmZK3Et9ioHkSoSODiCzNT1cRgsyQcYkhTDxlwBlgOTDs6.', 'fmi.baste@gmail.com', 5, '2019-01-29 14:07:02', 'A'),
(5, 5, 'jpcs.baste', '$2b$12$D9bEG7MoOiz2iaYDYez2a.LF3DhqhNXqtqgB/r/UkIHBfXmkuWj8y', 'sergeangelomajillo@gmail.com', 3, '2019-02-07 19:12:40', 'A'),
(6, 6, 'marulas', '$2b$12$DuUPMxNFzakvFc09wxEY2ONePp8T16Svj1MuiXGPVpVkodek.UICK', 'sergeangelomajillo@gmail.com', 4, '2019-02-07 19:14:56', 'A'),
(7, 7, 'salve.majillo', '$2b$12$SVLkqpUJ406lZM.eEOLXpO5BKpKU7AnfEzVOxDey5.uNbAUa7p1c.', 'sergeangelomajillo@gmail.com', 2, '2019-02-07 21:47:55', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `user_information`
--

CREATE TABLE `user_information` (
  `id` int(11) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `bio` varchar(160) DEFAULT NULL,
  `gender` char(1) NOT NULL,
  `birthday` date NOT NULL,
  `address` varchar(100) NOT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `partner_thrust` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_information`
--

INSERT INTO `user_information` (`id`, `first_name`, `middle_name`, `last_name`, `company_name`, `bio`, `gender`, `birthday`, `address`, `telephone`, `mobile_number`, `partner_thrust`) VALUES
(1, 'Ana', 'Dula', 'Manzano', 'San Sebastian College Recoletos de Cavite', 'I am the ReCOP Director.', 'F', '1998-01-21', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(2, 'Rafael', 'Something', 'Pecson', 'San Sebastian College Recoletos de Cavite', 'I am the President.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(3, 'James', 'Dexter', 'Tanquis', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Academics.', 'M', '2019-01-01', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(4, 'Cristituto', 'Somebody', 'Palomar', 'San Sebastian College Recoletos de Cavite', 'I am the VP for Finance.', 'M', '2019-01-29', 'Manila Boulevard, Brgy. 11 (Lawin) , J.Felipe Blvd, Santa Cruz, Cavite City, Cavite', NULL, NULL, 0),
(5, 'Antonio', 'Ching', 'Co', 'Junior Philippine Computer Society', 'I am checkered', 'M', '1998-01-21', 'San Sebastian College Recoletos de Cavite', '', '', 0),
(6, 'Serge Angelo', 'Isanan', 'Majillo', 'San Sebastian College Recoletos de Cavite', 'Please help!', 'M', '1998-01-21', 'Barangay Marulas', '', '', 0),
(7, 'Pauline Salve', 'Isanan', 'Majillo', 'WalterMart', 'I am pimps.', 'F', '1994-07-15', 'Centennial Rd, Kawit, Cavite', '', '', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_trail`
--
ALTER TABLE `audit_trail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `beneficiary`
--
ALTER TABLE `beneficiary`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `donation`
--
ALTER TABLE `donation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_attachment`
--
ALTER TABLE `event_attachment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_information`
--
ALTER TABLE `event_information`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_participation`
--
ALTER TABLE `event_participation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory_type`
--
ALTER TABLE `inventory_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `proposal_tracker`
--
ALTER TABLE `proposal_tracker`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `referral`
--
ALTER TABLE `referral`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_information`
--
ALTER TABLE `user_information`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_trail`
--
ALTER TABLE `audit_trail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `beneficiary`
--
ALTER TABLE `beneficiary`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `donation`
--
ALTER TABLE `donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_information`
--
ALTER TABLE `event_information`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `event_participation`
--
ALTER TABLE `event_participation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_type`
--
ALTER TABLE `inventory_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `proposal_tracker`
--
ALTER TABLE `proposal_tracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `referral`
--
ALTER TABLE `referral`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_account`
--
ALTER TABLE `user_account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_information`
--
ALTER TABLE `user_information`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
