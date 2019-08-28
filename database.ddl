CREATE TABLE IF NOT EXISTS Repositories(
RepoName varchar(50),
RepoDesc varchar(500),
RepoURL varchar(100),
primary key (RepoName)
);

INSERT INTO Repositories VALUES('test','test1','test2');
