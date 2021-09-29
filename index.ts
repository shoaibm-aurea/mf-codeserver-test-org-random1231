import simpleGit, { SimpleGit } from 'simple-git';

async function main() {
  const git = simpleGit(process.cwd());
  await git.pull();
  const branches = await git.branch(['-a']);
  console.log(branches);

  await git.branch(['-a']);
  await git.raw(['-a2']);
}

main();
