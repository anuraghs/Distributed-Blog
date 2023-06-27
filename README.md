# Distributed-Blog

Modeled a distributed blog post application where servers have the following features
 - Make a new post: given a username, a title, and the content, create a new blog post authored under the username with the title and the content
 - Comment on a post: given a username, a title, and a comment, if a blog post with the given title exists, create a new comment authored under the username for that post. Otherwise, the creation of the comment fails.
 - View all posts: list the title and the author for all blog posts in chronological order
 - View all posts made by a user: given a username, list the title and content of all blog posts made by this user in chronological order
 - View all comments on a post: given the title of a blog post, get its content, and list all the comments on the post and their authors

# Blockchain

Modeled the blog as a blockchain that acts as a log for all writing operations that have been applied to the blog. Blockchain implemented as a chain of blocks connected via hash pointers. A block consists of 3 fields:
 - A hash pointer (H)
 - Writing operation details (T)
 - Nonce (N)

# Consensus protocol

Implemented Multi-Paxos as the consensus protocol for replicating the blog and the blockchain across all servers. System handles crash failures and network failures. It is able to make progress as long as a majority of the nodes are alive and connected. A crashed node is able to restart, restore to its previous state from disk, and reconnect to the system. A partitioned node is able to reconnect with the rest of the system and resume normal operation. 
 - Restore from disk
 - Repair from other Nodes (servers)

Used TCP sockets for communication
