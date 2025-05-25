% report.cls

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Template for report in LaTeX for FCT NOVA
% Main class file
%
% Author: José Costa (https://github.com/zepedrocosta)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}

% Load the article class with some default options
\LoadClass[a4paper,12pt]{article}

% Required packages
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{helvet}
\RequirePackage{hyperref}
\RequirePackage{tocloft} % For customizing the table of contents
% \RequirePackage[portuguese]{babel} % Set language to Portuguese
\RequirePackage[utf8]{inputenc} % For UTF-8 encoding
\RequirePackage{lipsum} % For dummy text
\RequirePackage[backend=biber]{biblatex}
\RequirePackage{csquotes}
\RequirePackage{setspace}
\RequirePackage{xcolor}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Custom area
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set the variables for the title page
\newcommand{\university}{NOVA University of Lisbon}
\newcommand{\faculty}{NOVA School of Science and Technology}
\newcommand{\course}{MSC in Computer Science}
\newcommand{\project}{How do common open-source DBMSs perform under TPROC-C with fixed workloads}
\newcommand{\authorname}{José Costa (62637) \\ Rodrigo Albuquerque (70294) \\ Rodrigo Silva (70567)}
\newcommand{\subject}{Databases Systems}
\newcommand{\dateofsubmission}{\today} % Use \today for the current date

% Set the bibliography file
\addbibresource{bibliography.bib}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set default font to sans-serif
\renewcommand{\familydefault}{\sfdefault}

% Set page geometry
\geometry{a4paper, margin=1in}

% Custom table of contents
\setcounter{tocdepth}{4}

% Set the path for images
\graphicspath{{Images/}}

% Color for hyperlinks
\definecolor{darkblue}{rgb}{0.0,0.08,0.45}%
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,    % Color for internal links (e.g., TOC, \ref)
    citecolor=darkblue,    % Color for citation links
    urlcolor=darkblue      % Color for URL links
}
\PassOptionsToPackage{allcolors=darkblue}{hyperref}

% Custom title page
\newcommand{\maketitlepage}{
    \begin{titlepage}
        \centering

        \includegraphics[width=0.5\textwidth]{logo_nova_fct_en_v}\par

        \vspace{1cm}

        {\scshape\LARGE \university \par}

        \vspace{1cm}

        {\scshape\Large \course \par}

        \vspace{3cm}

        {\scshape\huge\bfseries \project \par}

        \vspace{2cm}

        {\Large\itshape \authorname \par}

        \vspace{3cm}

        {\scshape\large \subject \par}

        \vfill

        {\scshape\large \dateofsubmission \par}

        \doublespacing
        \tableofcontents
        \singlespacing

        \newpage
    \end{titlepage}
}

% Custom table of contents
\renewcommand{\cfttoctitlefont}{\huge\bfseries}
\renewcommand{\cftsecfont}{\large\bfseries}
\renewcommand{\cftsubsecfont}{\normalsize\bfseries}

% Custom section headings
\renewcommand{\section}{\@startsection{section}{1}{\z@}%
    {-3.5ex \@plus -1ex \@minus -.2ex}%
    {2.3ex \@plus.2ex}%
    {\normalfont\Large\bfseries}}

\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
    {-3.25ex \@plus -1ex \@minus -.2ex}%
    {1.5ex \@plus.2ex}%
    {\normalfont\large\bfseries}}

\endinput